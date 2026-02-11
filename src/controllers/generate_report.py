"""
FILE          : generate_report.py
PROJECT       : User-Activity-Analytics-Reporting-System
DESCRIPTION   :
    Command-line script to generate chart images and a PDF report
    from an existing SQLite database.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from Model.db import connect_db
from Model.analytics_sql import daily_active_users, top_features, events_per_day
from View.charts import generate_all_charts
from View.report import build_pdf_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate charts + PDF report from SQLite DB")
    parser.add_argument("--db", required=True, help="Path to SQLite DB (example: data\\activity.db)")
    parser.add_argument("--outdir", default="reports", help="Output folder (default: reports)")
    parser.add_argument("--title", default="User Activity Analytics Report", help="Report title")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    assets_dir = outdir / "assets"
    pdf_path = outdir / "output" / "activity_report.pdf"

    conn = connect_db(args.db)

    # Get data for tables
    dau_rows = daily_active_users(conn)
    feature_rows = top_features(conn, limit=5)
    events_rows = events_per_day(conn)

    # Create chart images
    chart_paths = generate_all_charts(conn, assets_dir)

    # Build the PDF
    build_pdf_report(
        pdf_path=pdf_path,
        title=args.title,
        dau_rows=dau_rows,
        top_feature_rows=feature_rows,
        events_per_day_rows=events_rows,
        chart_paths=chart_paths,
    )

    conn.close()
    print("Report created:", pdf_path)


if __name__ == "__main__":
    main()
