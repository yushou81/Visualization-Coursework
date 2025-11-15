#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import json

DATA_ROOT = Path("backend/InsiderThreatData/ITD-2018 Data Set")
DEPARTMENT_FILE = Path("backend/部门职位.csv")
IP_MAP_FILE = Path("backend/app/json_statics/ip_id.json")
WEBLOG_GROUP_FILE = Path("backend/app/json_statics/weblog_record_groups.json")

LOG_SPECS: Dict[str, Dict[str, object]] = {
    "login": {
        "filename": "login.csv",
        "columns": ["time", "user", "proto", "sip", "dip", "state"],
        "time_column": "time",
        "time_format": "%Y-%m-%d %H:%M:%S",
    },
    "weblog": {
        "filename": "weblog.csv",
        "columns": ["time", "sip", "host"],
        "time_column": "time",
        "time_format": "%Y-%m-%d %H:%M:%S",
    },
    "tcpLog": {
        "filename": "tcpLog.csv",
        "columns": ["stime", "dtime", "proto", "sip", "dip"],
        "time_column": "stime",
        "time_format": "%Y-%m-%d %H:%M:%S",
    },
    "email": {
        "filename": "email.csv",
        "columns": ["time", "from", "to", "subject"],
        "time_column": "time",
        "time_format": "%Y/%m/%d %H:%M",
    },
    "checking": {
        "filename": "checking.csv",
        "columns": ["day", "id", "checkin", "checkout"],
        "time_column": "day",
        "time_format": "%Y-%m-%d",
    },
}

KEYWORDS_SENSITIVE = ["方案", "源码", "机密", "敏感", "数据"]


def parse_dt(value: str, fmt: str) -> datetime | None:
    value = value.strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, fmt)
    except ValueError:
        return None


def read_text(path: Path, encodings: Tuple[str, ...] = ("utf-8", "utf-8-sig", "gb18030")) -> str:
    last_error: Exception | None = None
    for enc in encodings:
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError as exc:
            last_error = exc
            continue
    if last_error:
        raise last_error
    raise RuntimeError(f"Unable to read {path}")


def iter_csv_rows(path: Path, encodings: Tuple[str, ...] = ("utf-8", "utf-8-sig", "gb18030")) -> List[Dict[str, str]]:
    last_error: Exception | None = None
    for enc in encodings:
        try:
            with path.open("r", encoding=enc, errors="ignore", newline="") as fp:
                reader = csv.DictReader(fp)
                return list(reader)
        except UnicodeDecodeError as exc:
            last_error = exc
            continue
    if last_error:
        raise last_error
    return []


def scan_logs() -> Tuple[Dict[str, Dict[str, float]], Dict[str, Dict[str, int]]]:
    missing_rates: Dict[str, Dict[str, float]] = {}
    extra_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for log_name, spec in LOG_SPECS.items():
        filename = spec["filename"]  # type: ignore
        columns: List[str] = spec["columns"]  # type: ignore
        time_col = spec["time_column"]  # type: ignore
        time_fmt = spec["time_format"]  # type: ignore

        total_rows = 0
        missing_counts = defaultdict(int)
        offhour_count = 0
        weekend_count = 0
        sensitive_count = 0

        for day_dir in sorted(DATA_ROOT.iterdir()):
            if not day_dir.is_dir():
                continue
            file_path = day_dir / filename
            if not file_path.exists():
                continue
            with file_path.open("r", encoding="utf-8", errors="ignore", newline="") as fp:
                reader = csv.DictReader(fp)
                for row in reader:
                    total_rows += 1
                    for col in columns:
                        if not row.get(col, "").strip():
                            missing_counts[col] += 1
                    dt = parse_dt(row.get(time_col, ""), time_fmt)
                    if dt:
                        if log_name in {"login", "weblog", "tcpLog", "email"}:
                            hour = dt.hour
                            if hour < 7 or hour >= 20:
                                offhour_count += 1
                        if log_name in {"login", "weblog"}:
                            if dt.weekday() >= 5:
                                weekend_count += 1
                    if log_name == "email":
                        subj = row.get("subject", "")
                        if subj and any(keyword in subj for keyword in KEYWORDS_SENSITIVE):
                            sensitive_count += 1

        rates: Dict[str, float] = {}
        for col in columns:
            if total_rows == 0:
                rates[col] = 0.0
            else:
                rates[col] = missing_counts[col] / total_rows * 100.0
        missing_rates[log_name] = rates
        if log_name in {"login", "weblog", "tcpLog", "email"}:
            extra_stats[log_name]["offhour"] = offhour_count
        if log_name in {"login", "weblog"}:
            extra_stats[log_name]["weekend"] = weekend_count
        if log_name == "email":
            extra_stats[log_name]["sensitive_subject"] = sensitive_count

    return missing_rates, extra_stats


def compute_coverage() -> Dict[str, int]:
    coverage: Dict[str, int] = {}

    dept_text = read_text(DEPARTMENT_FILE)
    department_rows = max(0, len(dept_text.strip().splitlines()) - 1)
    coverage["organization_employees"] = department_rows

    ip_map = json.loads(read_text(IP_MAP_FILE))
    coverage["ip_mapped_users"] = len(ip_map)

    weblog_groups = json.loads(read_text(Path(WEBLOG_GROUP_FILE)))
    coverage["weblog_departments"] = len({entry.get("name") for entry in weblog_groups})

    # Simple anomaly cues: off-hour logins computed already, but here take unique user count in login outside office hours.
    login_offhour_users = set()
    login_file = LOG_SPECS["login"]
    filename = login_file["filename"]  # type: ignore
    time_col = login_file["time_column"]  # type: ignore
    time_fmt = login_file["time_format"]  # type: ignore
    for day_dir in sorted(DATA_ROOT.iterdir()):
        if not day_dir.is_dir():
            continue
        file_path = day_dir / filename
        if not file_path.exists():
            continue
        with file_path.open("r", encoding="utf-8", errors="ignore", newline="") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                dt = parse_dt(row.get(time_col, ""), time_fmt)
                if dt and (dt.hour < 7 or dt.hour >= 20):
                    user = row.get("user")
                    if user:
                        login_offhour_users.add(user)
    coverage["offhour_users"] = len(login_offhour_users)

    return coverage


def main() -> None:
    missing_rates, extra_stats = scan_logs()
    coverage = compute_coverage()

    print("=== Missing Rates (%, top columns) ===")
    for log, rates in missing_rates.items():
        top = sorted(rates.items(), key=lambda kv: kv[1], reverse=True)[:4]
        formatted = ", ".join(f"{k}:{v:.2f}%" for k, v in top)
        print(f"{log:8s}: {formatted}")

    print("\n=== Extra Stats ===")
    for log, stats in extra_stats.items():
        formatted = ", ".join(f"{k}={v}" for k, v in stats.items())
        print(f"{log:8s}: {formatted}")

    print("\n=== Coverage ===")
    for key, value in coverage.items():
        print(f"{key}: {value}")

    # Export to JSON for visualization
    payload = {
        "missing_rates": missing_rates,
        "extra_stats": extra_stats,
        "coverage": coverage,
    }
    Path("images").mkdir(exist_ok=True)
    Path("images/quality-metrics.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
