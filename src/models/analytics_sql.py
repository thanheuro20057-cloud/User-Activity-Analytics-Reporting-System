"""
FILE          : analytics_sql.py
PROJECT       : User-Activity-Analytics-Reporting-System
DESCRIPTION   :
    This file contains SQL query strings for analytics reports. 
    Each query is defined as a constant string variable.
    
"""

import sqlite3
from typing import List, Tuple

def daily_active_users(conn: sqlite3.Connection) -> List[Tuple[str, int]]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT DATE(event_ts) AS day, COUNT(DISTINCT user_id) AS dau
        FROM events
        GROUP BY day
        ORDER BY day;
        """
    )
    return cursor.fetchall()

def top_features(conn: sqlite3.Connection, limit: int = 10) -> List[Tuple[str, int]]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT feature, COUNT(*) AS usage_count
        FROM events
        GROUP BY feature
        ORDER BY usage_count DESC
        LIMIT ?;
        """,
        (limit,)
    )
    return cursor.fetchall()

def events_per_day(conn: sqlite3.Connection) -> List[Tuple[str, int]]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT DATE(event_ts) AS day, COUNT(*) AS event_count
        FROM events
        GROUP BY day
        ORDER BY day;
        """
    )
    return cursor.fetchall()