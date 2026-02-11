"""
FILE          : report.py
PROJECT       : User-Activity-Analytics-Reporting-System
DESCRIPTION   :
    Generates a PDF report using ReportLab, including summary tables and chart images.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def build_pdf_report(
    pdf_path: Path,
    title: str,
    dau_rows: List[Tuple[str, int]],
    top_feature_rows: List[Tuple[str, int]],
    events_per_day_rows: List[Tuple[str, int]],
    chart_paths: List[Path],
) -> Path:
    """
    Creates a PDF report and returns the path to the saved PDF.
    """
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 0.25 * inch))

    # DAU table
    story.append(Paragraph("Daily Active Users (DAU)", styles["Heading2"]))
    story.append(_make_table([("Day", "DAU")] + dau_rows))
    story.append(Spacer(1, 0.25 * inch))

    # Top features table
    story.append(Paragraph("Top Features", styles["Heading2"]))
    story.append(_make_table([("Feature", "Event Count")] + top_feature_rows))
    story.append(Spacer(1, 0.25 * inch))

    # Events/day table
    story.append(Paragraph("Events Per Day", styles["Heading2"]))
    story.append(_make_table([("Day", "Total Events")] + events_per_day_rows))
    story.append(Spacer(1, 0.25 * inch))

    # Charts (images)
    story.append(Paragraph("Charts", styles["Heading2"]))
    for p in chart_paths:
        if p.exists():
            story.append(Paragraph(p.name, styles["BodyText"]))
            story.append(Image(str(p), width=6.5 * inch, height=3.5 * inch))
            story.append(Spacer(1, 0.25 * inch))

    doc.build(story)
    return pdf_path


def _make_table(rows: List[Tuple]) -> Table:
    """
    Helper function: creates a formatted table for the PDF.
    """
    table = Table(rows)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table
