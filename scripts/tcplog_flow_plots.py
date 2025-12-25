#!/usr/bin/env python3
"""Plot TCP uplink/downlink comparisons and daily uplink trend."""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Dict, Tuple

import matplotlib.pyplot as plt


def scan_tcp(data_root: Path) -> Tuple[int, int, Dict[str, int], Dict[str, int]]:
    total_up = 0
    total_down = 0
    daily_up: Dict[str, int] = defaultdict(int)
    daily_down: Dict[str, int] = defaultdict(int)

    for day_dir in sorted(data_root.iterdir()):
        if not day_dir.is_dir():
            continue
        path = day_dir / "tcpLog.csv"
        if not path.exists():
            continue
        day = day_dir.name
        with path.open("r", encoding="utf-8", errors="ignore", newline="") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                try:
                    uplink = int(row.get("uplink_length") or 0)
                except ValueError:
                    uplink = 0
                try:
                    downlink = int(row.get("downlink_length") or 0)
                except ValueError:
                    downlink = 0
                total_up += uplink
                total_down += downlink
                daily_up[day] += uplink
                daily_down[day] += downlink
    return total_up, total_down, daily_up, daily_down


def plot(total_up: int, total_down: int, daily_up: Dict[str, int], output: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=140)

    axes[0].bar(["Uplink", "Downlink"], [total_up, total_down], color=["#2196f3", "#9c27b0"])
    axes[0].set_title("Total TCP Flow (Nov 2017)")
    axes[0].set_ylabel("Bytes")
    for idx, value in enumerate([total_up, total_down]):
        axes[0].text(idx, value * 1.01, f"{value/1e12:.2f}e12B", ha="center")

    days = sorted(daily_up.keys())
    daily_vals = [daily_up[day] for day in days]
    axes[1].plot(days, daily_vals, marker="o", color="#ff5722")
    axes[1].set_title("Daily TCP Uplink Volume")
    axes[1].set_ylabel("Bytes")
    axes[1].set_xlabel("Date (2017-11)")
    axes[1].tick_params(axis="x", rotation=60)
    axes[1].grid(alpha=0.3)

    if "2017-11-24" in daily_up:
        peak = daily_up["2017-11-24"]
        axes[1].axvline("2017-11-24", color="#4caf50", linestyle="--", alpha=0.6)
        axes[1].annotate(
            f"11-24: {peak/1e9:.2f} GB",
            xy=("2017-11-24", peak),
            xytext=(-30, 30),
            textcoords="offset points",
            arrowprops=dict(arrowstyle="->", color="#4caf50"),
            fontsize=9,
        )

    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output)
    print(f"Saved TCP flow plots to {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP flow plots.")
    parser.add_argument(
        "--data-root",
        type=Path,
        default=Path("backend/InsiderThreatData/ITD-2018 Data Set"),
        help="Directory containing 2017-11-* folders",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("images/tcplog_flow_plots.png"),
        help="Output image path",
    )
    args = parser.parse_args()

    total_up, total_down, daily_up, daily_down = scan_tcp(args.data_root)
    plot(total_up, total_down, daily_up, args.output)


if __name__ == "__main__":
    main()
