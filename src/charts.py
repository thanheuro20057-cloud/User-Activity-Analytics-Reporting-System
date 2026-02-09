"""
FILE          : charts.py
PROJECT       : User-Activity-Analytics-Reporting-System
DESCRIPTION   :
    Generates chart images (PNG) from analytics data stored in SQLite.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import sqlite3

from src.analytics_sql import daily_active_users, events_per_day, top_features


def save_dau_chart(conn: sqlite3.Connection, output_path: Path) -> Path:
    """
    Creates a line chart for DAU (Daily Active Users) and saves it as a PNG.

    Returns the path to the saved image.
    """
    results: List[Tuple[str, int]] = daily_active_users(conn)
    days = [row[0] for row in results]
    dau_values = [row[1] for row in results]

    plt.figure()
    plt.plot(days, dau_values, marker="o")
    plt.title("Daily Active Users (DAU)")
    plt.xlabel("Day")
    plt.ylabel("Unique Users")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()

    return output_path


def save_top_features_chart(conn: sqlite3.Connection, output_path: Path, limit: int = 5) -> Path:
    """
    Creates a bar chart for top feature usage and saves it as a PNG.

    Returns the path to the saved image.
    """
    results: List[Tuple[str, int]] = top_features(conn, limit=limit)
    features = [row[0] for row in results]
    counts = [row[1] for row in results]

    plt.figure()
    plt.bar(features, counts)
    plt.title(f"Top {limit} Features (by Events)")
    plt.xlabel("Feature")
    plt.ylabel("Event Count")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()

    return output_path


def save_events_per_day_chart(conn: sqlite3.Connection, output_path: Path) -> Path:
    """
    Creates a bar chart for total events per day and saves it as a PNG.

    Returns the path to the saved image.
    """
    results: List[Tuple[str, int]] = events_per_day(conn)
    days = [row[0] for row in results]
    totals = [row[1] for row in results]

    plt.figure()
    plt.bar(days, totals)
    plt.title("Total Events Per Day")
    plt.xlabel("Day")
    plt.ylabel("Total Events")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()

    return output_path


def generate_all_charts(conn: sqlite3.Connection, assets_dir: Path) -> List[Path]:
    """
    Generates all charts and returns a list of paths to the PNG files.
    """
    chart_paths: List[Path] = []

    chart_paths.append(save_dau_chart(conn, assets_dir / "dau.png"))
    chart_paths.append(save_top_features_chart(conn, assets_dir / "top_features.png", limit=5))
    chart_paths.append(save_events_per_day_chart(conn, assets_dir / "events_per_day.png"))

    return chart_paths
