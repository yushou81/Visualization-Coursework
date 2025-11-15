#!/usr/bin/env python3
"""Utility for loading the ITD-2018 CSV data set into MySQL.

The script performs the following tasks:
  * Imports static reference data (link / department tables).
  * Streams all daily CSV files (email, weblog, login, tcpLog, checking).
  * Builds helper tables (urldomain, domain_tag) and aggregated weblog_record data.

It is intentionally self-contained so it can run inside WSL while the
database is hosted on Windows.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Tuple

import pymysql


DEFAULT_DATA_ROOT = Path("InsiderThreatData/ITD-2018 Data Set")
DEFAULT_DEPARTMENT_FILE = Path("部门职位.csv")
DEFAULT_IP_FILE = Path("app/json_statics/ip_id.json")
DEFAULT_DEPART_FILE = Path("app/json_statics/weblog_record_users.json")


@dataclass
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


class DomainClassifier:
    """Rudimentary domain -> tag classifier with keyword rules."""

    CATEGORY_KEYWORDS = {
        "办公": [
            "hightech.com",
            "oa.",
            "email.",
            "lib0",
            "vpn",
            "crm",
            "jira",
            "intra",
        ],
        "开发": [
            "git",
            "jenkins",
            "maven",
            "api",
            "dev",
            "ci",
            "build",
            "code",
        ],
        "技术": [
            "github",
            "stackoverflow",
            "csdn",
            "51cto",
            "segmentfault",
            "kaggle",
            "ibm.com",
            "oracle.com",
        ],
        "娱乐": [
            "youku",
            "qq.com",
            "weibo",
            "bilibili",
            "acfun",
            "game",
            "nba",
            "music",
            "video",
            "sina.com.cn",
            "17173",
            "hupu",
        ],
        "购物": [
            "amazon",
            "jd.com",
            "tmall",
            "taobao",
            "dangdang",
            "suning",
            "gome",
            "vip.com",
        ],
        "招聘": [
            "51job",
            "liepin",
            "zhaopin",
            "lagou",
            "kanzhun",
            "job5156",
            "sunhr",
            "boss",
        ],
        "搜索": [
            "baidu",
            "google",
            "bing",
            "sogou",
            "so.com",
            "yahoo",
        ],
        "赌博": [
            "bet",
            "casino",
            "lottery",
            "poker",
        ],
    }

    DEFAULT_FALLBACK = "娱乐"

    def classify(self, host: str) -> str:
        lower = host.lower()
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in lower:
                    return category
        if "hightech" in lower:
            return "办公"
        return self.DEFAULT_FALLBACK


class ChinavisImporter:
    def __init__(self, *,
                 db: DbConfig,
                 data_root: Path,
                 department_file: Path,
                 ip_map_file: Path,
                 depart_map_file: Path,
                 batch_size: int,
                 truncate: bool) -> None:
        self.db_config = db
        self.data_root = data_root
        self.department_file = department_file
        self.ip_map_file = ip_map_file
        self.depart_map_file = depart_map_file
        self.batch_size = batch_size
        self.truncate = truncate

        self.connection = self._create_connection()
        self.connection.autocommit(False)
        self.cursor = self.connection.cursor()

        self.id_to_ip: Dict[str, str] = {}
        self.ip_to_id: Dict[str, str] = {}
        self.id_to_depart_code: Dict[str, str] = {}
        self.url_to_domain: Dict[str, str] = {}
        self.domain_to_tag: Dict[str, str] = {}
        self.tag_counter = defaultdict(lambda: defaultdict(int))
        self.classifier = DomainClassifier()

    # ------------------------------------------------------------------
    def _create_connection(self) -> pymysql.connections.Connection:
        return pymysql.connect(
            host=self.db_config.host,
            port=self.db_config.port,
            user=self.db_config.user,
            password=self.db_config.password,
            db=self.db_config.database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.Cursor,
        )

    # ------------------------------------------------------------------
    def run(self) -> None:
        try:
            self._load_mappings()
            if self.truncate:
                self._truncate_tables()
            self._load_reference_tables()
            self._ingest_checking()
            self._ingest_email()
            self._ingest_weblog()
            self._ingest_login()
            self._ingest_tcplog()
            self._persist_domain_helpers()
            self._persist_weblog_record()
            self.connection.commit()
        finally:
            self.cursor.close()
            self.connection.close()

    # ------------------------------------------------------------------
    def _load_mappings(self) -> None:
        self._log(f"Loading IP map from {self.ip_map_file}")
        ip_data = json.loads(self.ip_map_file.read_text(encoding="utf-8"))
        for entry in ip_data:
            user_id = entry["id"].strip()
            ip = entry["ip"].strip()
            self.id_to_ip[user_id] = ip
            self.ip_to_id[ip] = user_id

        self._log(f"Loading depart codes from {self.depart_map_file}")
        depart_rows = json.loads(self.depart_map_file.read_text(encoding="utf-8"))
        for row in depart_rows:
            self.id_to_depart_code[str(row["name"])]=row.get("depart","0")

    # ------------------------------------------------------------------
    def _truncate_tables(self) -> None:
        tables = [
            "email",
            "weblog",
            "login",
            "tcpLog",
            "checking2",
            "department",
            "link",
            "urldomain",
            "domain_tag",
            "weblog_record",
        ]
        self._log("Truncating existing data")
        self.cursor.execute("SET FOREIGN_KEY_CHECKS=0")
        for table in tables:
            self.cursor.execute(f"TRUNCATE TABLE {table}")
        self.cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        self.connection.commit()

    # ------------------------------------------------------------------
    def _load_reference_tables(self) -> None:
        self._log("Loading department/link reference data")
        rows = list(self._read_csv(self.department_file, encodings=("utf-8-sig", "gb18030", "latin1")))
        dept_stmt = "REPLACE INTO department (id, department, position) VALUES (%s, %s, %s)"
        link_stmt = "REPLACE INTO link (id, ip, email, level, depart) VALUES (%s, %s, %s, %s, %s)"
        dept_payload = []
        link_payload = []
        for row in rows:
            user_id = row["id"].strip()
            email = row["email"].strip().lower()
            department_name = row["department"].strip()
            position = row["position"].strip()
            ip = self.id_to_ip.get(user_id)
            if not ip:
                self._log(f"Skipping user {user_id}, no IP mapping found", error=True)
                continue
            level = self._derive_level(position)
            depart_code = self.id_to_depart_code.get(user_id) or self._guess_depart_code(department_name)
            dept_payload.append((user_id, department_name, position))
            link_payload.append((user_id, ip, email, level, depart_code))

        if dept_payload:
            self.cursor.executemany(dept_stmt, dept_payload)
        if link_payload:
            self.cursor.executemany(link_stmt, link_payload)
        self.connection.commit()

    # ------------------------------------------------------------------
    def _ingest_email(self) -> None:
        self._log("Importing email logs")
        insert_sql = (
            "INSERT INTO email (time, proto, sip, sport, dip, dport, sender, receiver, subject) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        )
        for path in self._daily_files("email.csv"):
            batch = []
            for row in self._read_csv(path, encodings=("utf-8-sig", "gb18030", "latin1")):
                batch.append((
                    self._parse_dt(row["time"], "%Y/%m/%d %H:%M"),
                    row["proto"],
                    row["sip"],
                    self._to_int(row["sport"]),
                    row["dip"],
                    self._to_int(row["dport"]),
                    row["from"],
                    row["to"],
                    row["subject"],
                ))
                if len(batch) >= self.batch_size:
                    self.cursor.executemany(insert_sql, batch)
                    batch.clear()
            if batch:
                self.cursor.executemany(insert_sql, batch)
            self.connection.commit()

    # ------------------------------------------------------------------
    def _ingest_weblog(self) -> None:
        self._log("Importing weblog entries")
        insert_sql = (
            "INSERT INTO weblog (time, sip, sport, dip, dport, host) VALUES (%s,%s,%s,%s,%s,%s)"
        )
        for path in self._daily_files("weblog.csv"):
            batch = []
            for row in self._read_csv(path):
                host = row["host"].strip()
                time_value = self._parse_dt(row["time"], "%Y-%m-%d %H:%M:%S")
                sport = self._to_int(row["sport"])
                dport = self._to_int(row["dport"])
                batch.append((time_value, row["sip"], sport, row["dip"], dport, host))
                self._handle_weblog_side_effects(row["sip"], host)
                if len(batch) >= self.batch_size:
                    self.cursor.executemany(insert_sql, batch)
                    batch.clear()
            if batch:
                self.cursor.executemany(insert_sql, batch)
            self.connection.commit()

    # ------------------------------------------------------------------
    def _ingest_login(self) -> None:
        self._log("Importing login records")
        insert_sql = (
            "INSERT INTO login (time, user, proto, sip, sport, dip, dport, state) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        )
        for path in self._daily_files("login.csv"):
            batch = []
            for row in self._read_csv(path):
                batch.append((
                    self._parse_dt(row["time"], "%Y-%m-%d %H:%M:%S"),
                    row["user"],
                    row["proto"],
                    row["sip"],
                    self._to_int(row["sport"]),
                    row["dip"],
                    self._to_int(row["dport"]),
                    row["state"],
                ))
                if len(batch) >= self.batch_size:
                    self.cursor.executemany(insert_sql, batch)
                    batch.clear()
            if batch:
                self.cursor.executemany(insert_sql, batch)
            self.connection.commit()

    # ------------------------------------------------------------------
    def _ingest_tcplog(self) -> None:
        self._log("Importing TCP logs")
        insert_sql = (
            "INSERT INTO tcpLog (stime, dtime, proto, sip, sport, dip, dport, uplink_length, downlink_length) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        )
        for path in self._daily_files("tcpLog.csv"):
            batch = []
            for row in self._read_csv(path):
                batch.append((
                    self._parse_dt(row["stime"], "%Y-%m-%d %H:%M:%S"),
                    self._parse_dt(row["dtime"], "%Y-%m-%d %H:%M:%S"),
                    row["proto"],
                    row["sip"],
                    self._to_int(row["sport"]),
                    row["dip"],
                    self._to_int(row["dport"]),
                    self._to_int(row["uplink_length"]),
                    self._to_int(row["downlink_length"]),
                ))
                if len(batch) >= self.batch_size:
                    self.cursor.executemany(insert_sql, batch)
                    batch.clear()
            if batch:
                self.cursor.executemany(insert_sql, batch)
            self.connection.commit()

    # ------------------------------------------------------------------
    def _ingest_checking(self) -> None:
        self._log("Importing checking records")
        insert_sql = (
            "INSERT INTO checking2 (id, day, checkin, checkout) VALUES (%s,%s,%s,%s)"
        )
        for path in self._daily_files("checking.csv"):
            batch = []
            for row in self._read_csv(path):
                batch.append((
                    row["id"],
                    self._parse_dt(row["day"], "%Y-%m-%d").date(),
                    row["checkin"],
                    row["checkout"],
                ))
                if len(batch) >= self.batch_size:
                    self.cursor.executemany(insert_sql, batch)
                    batch.clear()
            if batch:
                self.cursor.executemany(insert_sql, batch)
            self.connection.commit()

    # ------------------------------------------------------------------
    def _persist_domain_helpers(self) -> None:
        self._log("Persisting URL/domain helper tables")
        url_stmt = "REPLACE INTO urldomain (url, domain) VALUES (%s, %s)"
        domain_stmt = "REPLACE INTO domain_tag (domain, tag) VALUES (%s, %s)"
        url_pairs = list(self.url_to_domain.items())
        if url_pairs:
            self.cursor.executemany(url_stmt, url_pairs)
        domain_pairs = list(self.domain_to_tag.items())
        if domain_pairs:
            self.cursor.executemany(domain_stmt, domain_pairs)
        self.connection.commit()

    # ------------------------------------------------------------------
    def _persist_weblog_record(self) -> None:
        self._log("Persisting aggregated weblog_record table")
        insert_sql = "REPLACE INTO weblog_record (depart, id, tag, record) VALUES (%s,%s,%s,%s)"
        payload = []
        for user_id, tag_dict in self.tag_counter.items():
            depart_code = self.id_to_depart_code.get(user_id, "0")
            for tag, count in tag_dict.items():
                payload.append((depart_code, user_id, tag, count))
        if payload:
            self.cursor.executemany(insert_sql, payload)
        self.connection.commit()

    # ------------------------------------------------------------------
    def _handle_weblog_side_effects(self, sip: str, host: str) -> None:
        canonical = self._canonical_domain(host)
        self.url_to_domain.setdefault(host, canonical)
        tag = self.classifier.classify(host)
        self.domain_to_tag.setdefault(canonical, tag)
        user_id = self.ip_to_id.get(sip)
        if user_id:
            self.tag_counter[user_id][tag] += 1

    # ------------------------------------------------------------------
    def _read_csv(self, path: Path, encodings: Tuple[str, ...] = ("utf-8-sig", "gb18030")) -> Iterator[Dict[str, str]]:
        last_error: Optional[Exception] = None
        for enc in encodings:
            try:
                with path.open("r", encoding=enc, newline="") as fp:
                    reader = csv.DictReader(fp)
                    for row in reader:
                        yield {k.strip(): v.strip() for k, v in row.items()}
                return
            except UnicodeDecodeError as err:
                last_error = err
                continue
        raise last_error  # type: ignore

    # ------------------------------------------------------------------
    def _daily_files(self, filename: str) -> Iterable[Path]:
        for day_dir in sorted(self.data_root.iterdir()):
            if not day_dir.is_dir():
                continue
            path = day_dir / filename
            if path.exists():
                yield path

    # ------------------------------------------------------------------
    @staticmethod
    def _parse_dt(value: str, fmt: str) -> datetime:
        value = value.strip()
        return datetime.strptime(value, fmt)

    @staticmethod
    def _to_int(value: str) -> Optional[int]:
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _derive_level(position: str) -> int:
        if "总经理" in position:
            return 4
        if "部长" in position:
            return 3
        if "组长" in position or "主管" in position:
            return 2
        return 1

    @staticmethod
    def _guess_depart_code(department_name: str) -> str:
        mapping = {
            "管理": "0",
            "人力": "1",
            "财务": "2",
            "研发1": "3.1",
            "研发2": "3.2",
            "研发3": "3.3",
            "研发": "3",
        }
        for key, value in mapping.items():
            if key in department_name:
                return value
        return "0"

    @staticmethod
    def _canonical_domain(host: str) -> str:
        host = host.lower().split("/")[0]
        parts = [part for part in host.split(".") if part]
        if len(parts) <= 2:
            return host
        # Handle multi-level TLDs such as .com.cn
        second_level = {"com", "net", "org", "gov", "edu"}
        country_codes = {"cn", "hk", "uk"}
        if parts[-2] in second_level and parts[-1] in country_codes:
            return ".".join(parts[-3:])
        return ".".join(parts[-2:])

    def _log(self, message: str, *, error: bool = False) -> None:
        stream = sys.stderr if error else sys.stdout
        stream.write(f"[import] {message}\n")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import ITD-2018 CSV data into MySQL")
    parser.add_argument("--db-host", default="127.0.0.1")
    parser.add_argument("--db-port", type=int, default=3306)
    parser.add_argument("--db-user", default="chinavis")
    parser.add_argument("--db-pass", default="chinavis2018")
    parser.add_argument("--db-name", default="chinavis")
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--department-file", type=Path, default=DEFAULT_DEPARTMENT_FILE)
    parser.add_argument("--ip-map-file", type=Path, default=DEFAULT_IP_FILE)
    parser.add_argument("--depart-map-file", type=Path, default=DEFAULT_DEPART_FILE)
    parser.add_argument("--batch-size", type=int, default=2000)
    parser.add_argument("--truncate", action="store_true", help="Truncate tables before importing")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    importer = ChinavisImporter(
        db=DbConfig(
            host=args.db_host,
            port=args.db_port,
            user=args.db_user,
            password=args.db_pass,
            database=args.db_name,
        ),
        data_root=args.data_root,
        department_file=args.department_file,
        ip_map_file=args.ip_map_file,
        depart_map_file=args.depart_map_file,
        batch_size=args.batch_size,
        truncate=args.truncate,
    )
    importer.run()


if __name__ == "__main__":
    main()
