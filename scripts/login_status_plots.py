#!/usr/bin/env python3
"""Plot login success/failure pie chart and daily failure bar chart."""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt


def scan_login(data_root: Path) -> tuple[Dict[str, int], Dict[str, int]]:
    state_counts: Dict[str, int] = defaultdict(int)
    daily_failures: Dict[str, int] = defaultdict(int)
    for day_dir in sorted(data_root.iterdir()):
        if not day_dir.is_dir():
            continue
        login_path = day_dir / "login.csv"
        if not login_path.exists():
            continue
        day = day_dir.name
        with login_path.open("r", encoding="utf-8", errors="ignore", newline="") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                state = (row.get("state") or "").strip().lower()
                state_counts[state] += 1
                if state not in {"success"}:
                    daily_failures[day] += 1
    return state_counts, daily_failures


def plot(state_counts: Dict[str, int], daily_failures: Dict[str, int], output: Path) -> None:
    success = state_counts.get("success", 0)
    failure = sum(count for state, count in state_counts.items() if state != "success")

    days = sorted(daily_failures.keys())
    failure_counts = [daily_failures[day] for day in days]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=140)

    axes[0].pie(
        [success, failure],
        labels=[f"Success ({success})", f"Failure ({failure})"],
        autopct="%1.1f%%",
        colors=["#4caf50", "#f44336"],
        startangle=90,
    )
    axes[0].set_title("Login Status Distribution (Nov 2017)")

    axes[1].bar(days, failure_counts, color="#ff9800")
    axes[1].set_title("Daily Login Failures")
    axes[1].set_ylabel("Failure count")
    axes[1].set_xlabel("Date (2017-11)")
    axes[1].tick_params(axis="x", rotation=60)
    axes[1].grid(axis="y", alpha=0.3)

    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output)
    print(f"Saved plot to {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Login success/failure plots.")
    parser.add_argument(
        "--data-root",
        type=Path,
        default=Path("backend/InsiderThreatData/ITD-2018 Data Set"),
        help="Directory containing 2017-11-* folders",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("images/login_status_plots.png"),
        help="Output plot path",
    )
    args = parser.parse_args()
    state_counts, daily_failures = scan_login(args.data_root)
    plot(state_counts, daily_failures, args.output)


if __name__ == "__main__":
    main()
