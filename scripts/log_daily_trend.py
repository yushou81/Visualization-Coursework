#!/usr/bin/env python3
"""Plot daily totals for all five log types across November 2017."""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict, OrderedDict
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt

LOG_TYPES = OrderedDict(
    [
        ("login", "Login"),
        ("weblog", "Web access"),
        ("tcpLog", "TCP flow"),
        ("email", "Email"),
        ("checking", "Checking"),
    ]
)


def count_rows_per_day(data_root: Path) -> tuple[Dict[str, Dict[str, int]], List[str]]:
    """Return ({log_type: {day: count}}, sorted days)."""
    stats: Dict[str, Dict[str, int]] = {
        name: defaultdict(int) for name in LOG_TYPES.keys()
    }
    day_names: List[str] = []
    for day_dir in sorted(data_root.iterdir()):
        if not day_dir.is_dir():
            continue
        day = day_dir.name
        day_names.append(day)
        for log_name in LOG_TYPES.keys():
            file_path = day_dir / f"{log_name}.csv"
            if not file_path.exists():
                continue
            with file_path.open("r", encoding="utf-8", errors="ignore", newline="") as fp:
                reader = csv.reader(fp)
                try:
                    next(reader)  # header
                except StopIteration:
                    continue
                stats[log_name][day] += sum(1 for _ in reader)
    return stats, day_names


def plot(stats: Dict[str, Dict[str, int]], days: List[str], output: Path) -> None:
    fig, ax = plt.subplots(figsize=(12, 6), dpi=140)
    color_cycle = plt.rcParams["axes.prop_cycle"].by_key().get("color", [])
    for idx, (log_name, label) in enumerate(LOG_TYPES.items()):
        counts = [stats[log_name].get(day, 0) for day in days]
        ax.plot(
            days,
            counts,
            label=f"{label} ({log_name})",
            linewidth=1.8,
            color=color_cycle[idx % len(color_cycle)],
            marker="o",
            markersize=3,
        )
    ax.set_title("HighTech 2017-11 Daily Log Volume")
    ax.set_ylabel("Records")
    ax.set_xlabel("Date (2017-11)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output)
    print(f"Trend chart saved to {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot daily totals for logs.")
    parser.add_argument(
        "--data-root",
        type=Path,
        default=Path("backend/InsiderThreatData/ITD-2018 Data Set"),
        help="Directory containing 2017-11-* subdirectories",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("images/log_daily_trend.png"),
        help="Output image path",
    )
    args = parser.parse_args()
    stats, days = count_rows_per_day(args.data_root)
    unique_days = list(dict.fromkeys(days))
    plot(stats, unique_days, args.output)


if __name__ == "__main__":
    main()
