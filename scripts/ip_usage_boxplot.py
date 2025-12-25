#!/usr/bin/env python3
"""Compute employee ↔ IP usage stats and draw boxplots.

The script scans all login.csv files under the specified data root,
counts how many distinct source IPs each employee使用, and how many
employees share each source IP. Results are printed and plotted.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List
import random

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    plt = None


def iter_login_rows(data_root: Path) -> Iterable[Dict[str, str]]:
    """Yield rows from every login.csv under day directories."""
    for day_dir in sorted(data_root.iterdir()):
        if not day_dir.is_dir():
            continue
        login_path = day_dir / "login.csv"
        if not login_path.exists():
            continue
        with login_path.open("r", encoding="utf-8", errors="ignore", newline="") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                yield row


def main() -> None:
    parser = argparse.ArgumentParser(description="Employee-IP usage distribution")
    parser.add_argument(
        "--data-root",
        default="backend/InsiderThreatData/ITD-2018 Data Set",
        type=Path,
        help="Root directory containing 2017-11-* day folders",
    )
    parser.add_argument(
        "--output",
        default="images/ip_usage_boxplot.png",
        type=Path,
        help="Path to save the boxplot figure",
    )
    args = parser.parse_args()

    user_ips: Dict[str, set[str]] = defaultdict(set)
    ip_users: Dict[str, set[str]] = defaultdict(set)

    total_rows = 0
    for row in iter_login_rows(args.data_root):
        total_rows += 1
        user = (row.get("user") or "").strip()
        sip = (row.get("sip") or "").strip()
        if not user or not sip:
            continue
        user_ips[user].add(sip)
        ip_users[sip].add(user)

    user_ip_counts: List[int] = [len(ips) for ips in user_ips.values() if ips]
    ip_user_counts: List[int] = [len(users) for users in ip_users.values() if users]

    print(f"Processed login rows: {total_rows}")
    print(f"Employees with login entries: {len(user_ip_counts)}")
    print(f"IPs observed: {len(ip_user_counts)}")
    if user_ip_counts:
        print(
            f"Employee distinct IPs — min:{min(user_ip_counts)}, "
            f"median:{sorted(user_ip_counts)[len(user_ip_counts)//2]}, "
            f"max:{max(user_ip_counts)}"
        )
    if ip_user_counts:
        print(
            f"IP shared by employees — min:{min(ip_user_counts)}, "
            f"median:{sorted(ip_user_counts)[len(ip_user_counts)//2]}, "
            f"max:{max(ip_user_counts)}"
        )

    if plt:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=120)
        rng = random.Random(42)

        def draw_panel(ax, data: List[int], title: str, ylabel: str) -> None:
            ax.boxplot(data, vert=True, patch_artist=True, widths=0.15)
            ax.set_xticks([1])
            ax.set_xticklabels([""])
            ax.set_title(title)
            ax.set_ylabel(ylabel)
            ax.set_ylim(0, max(data) + 1)
            # jittered swarm to show discrete counts
            for value in data:
                jitter = (rng.random() - 0.5) * 0.2
                ax.scatter(1 + jitter, value, color="#1f77b4", alpha=0.25, s=15)
            freq = Counter(data)
            for value, count in sorted(freq.items()):
                ax.text(
                    1.15,
                    value,
                    f"{count}×",
                    va="center",
                    fontsize=8,
                    color="#444",
                )
            ax.grid(axis="y", linestyle="--", alpha=0.4)

        draw_panel(
            axes[0],
            user_ip_counts,
            "Employee → distinct source IPs",
            "Distinct IP count per employee",
        )
        draw_panel(
            axes[1],
            ip_user_counts,
            "Source IP → distinct employees",
            "Distinct employee count per IP",
        )

        fig.suptitle("HighTech 2017-11 Login Employee-IP Usage Distribution")
        fig.tight_layout()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.output)
        print(f"Boxplot saved to {args.output}")
    else:
        print(
            "matplotlib is not installed; skipped boxplot generation. "
            "Install matplotlib to produce the figure."
        )


if __name__ == "__main__":
    main()
