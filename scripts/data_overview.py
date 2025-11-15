#!/usr/bin/env python3
from pathlib import Path
import csv
from datetime import datetime

DATA_ROOT = Path("backend/InsiderThreatData/ITD-2018 Data Set")
LOG_SPECS = {
    "weblog":  {"filename": "weblog.csv",  "columns": ["time"],        "formats": ["%Y-%m-%d %H:%M:%S"]},
    "login":   {"filename": "login.csv",   "columns": ["time"],        "formats": ["%Y-%m-%d %H:%M:%S"]},
    "tcpLog":  {"filename": "tcpLog.csv",  "columns": ["stime","dtime"],"formats": ["%Y-%m-%d %H:%M:%S"]},
    "email":   {"filename": "email.csv",   "columns": ["time"],        "formats": ["%Y/%m/%d %H:%M"]},
    "checking":{"filename": "checking.csv","columns": ["day"],         "formats": ["%Y-%m-%d"]},
}

def parse_dt(value, formats):
    value = value.strip()
    if not value:
        return None
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None

records = []
for log_name, spec in LOG_SPECS.items():
    total_rows = 0
    min_ts = None
    max_ts = None
    for day_dir in sorted(DATA_ROOT.iterdir()):
        if not day_dir.is_dir():
            continue
        file_path = day_dir / spec["filename"]
        if not file_path.exists():
            continue
        with file_path.open("r", encoding="utf-8", errors="ignore", newline="") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                total_rows += 1
                for col in spec["columns"]:
                    dt = parse_dt(row.get(col, ""), spec["formats"])
                    if dt is None:
                        continue
                    if min_ts is None or dt < min_ts:
                        min_ts = dt
                    if max_ts is None or dt > max_ts:
                        max_ts = dt
    records.append({"log": log_name, "rows": total_rows, "start": min_ts, "end": max_ts})

records.sort(key=lambda x: x["rows"], reverse=True)

for rec in records:
    start = rec["start"].strftime("%Y-%m-%d") if rec["start"] else "N/A"
    end = rec["end"].strftime("%Y-%m-%d") if rec["end"] else "N/A"
    print(f"{rec['log']:8s} rows={rec['rows']:>8,d} range={start} -> {end}")

max_rows = max(r["rows"] for r in records)
width, height = 900, 450
left_margin, bottom_margin = 80, 90
bar_width, bar_gap = 80, 50
colors = ["#6c8ebf", "#82b366", "#d6b656", "#b85450", "#9673a6"]

svg_lines = [
    '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
    '<rect width="100%" height="100%" fill="#ffffff"/>',
    '<text x="450" y="40" font-size="24" text-anchor="middle" fill="#333">2017-11 日志规模概览</text>',
]

max_bar_height = height - bottom_margin - 60
x = left_margin
for idx, rec in enumerate(records):
    bar_height = 0 if max_rows == 0 else int(rec["rows"] / max_rows * max_bar_height)
    y = height - bottom_margin - bar_height
    color = colors[idx % len(colors)]
    svg_lines.append(f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{color}" rx="6" ry="6"/>')
    svg_lines.append(f'<text x="{x + bar_width/2}" y="{height - bottom_margin + 20}" font-size="14" text-anchor="middle" fill="#333">{rec["log"]}</text>')
    svg_lines.append(f'<text x="{x + bar_width/2}" y="{y - 6}" font-size="12" text-anchor="middle" fill="#333">{rec["rows"]:,}</text>')
    if rec["start"] and rec["end"]:
        timeline = f"{rec['start'].strftime('%m-%d')} → {rec['end'].strftime('%m-%d')}"
    else:
        timeline = "N/A"
    svg_lines.append(f'<text x="{x + bar_width/2}" y="{height - bottom_margin + 40}" font-size="11" text-anchor="middle" fill="#666">{timeline}</text>')
    x += bar_width + bar_gap

svg_lines.append("</svg>")
Path("images").mkdir(exist_ok=True)
Path("images/data-overview.svg").write_text("\n".join(svg_lines), encoding="utf-8")
