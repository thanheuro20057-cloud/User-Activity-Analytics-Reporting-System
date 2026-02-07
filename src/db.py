"""
FILE          : db.py
PROJECT       : User-Activity-Analytics-Reporting-System
DESCRIPTION   :
    This file contains database helper functions for SQLite:
    - connect_db: opens/creates the database file
    - init_db: creates the events table if it does not exist
    - insert_events: inserts many event rows into the events table
"""

import sqlite3
from typing import List, Tuple


def connect_db(db_path: str) -> sqlite3.Connection:
    """
    FUNCTION    : connect_db
    DESCRIPTION : Opens (or creates) the SQLite database file and returns a connection object.
    PARAMETERS  : db_path (str) - path to the database file (example: data/activity.db)
    RETURNS     : sqlite3.Connection - connection used to run SQL commands
    """
    return sqlite3.connect(db_path)


def init_db(conn: sqlite3.Connection) -> None:
    """
    FUNCTION    : init_db
    DESCRIPTION : Creates the events table if it does not exist.
    PARAMETERS  : conn (sqlite3.Connection) - open database connection
    RETURNS     : None
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_ts TEXT NOT NULL,
            user_id TEXT NOT NULL,
            feature TEXT NOT NULL,
            event_type TEXT NOT NULL,
            session_id TEXT
        );
        
        """
    conn.execute(
        """
            CREATE UNIQUE INDEX IF NOT EXISTS ux_events_natural
            ON events (event_ts, user_id, feature, event_type, session_id);
        """
        
    )

        
    )
    conn.commit()


def insert_events(conn: sqlite3.Connection, rows: List[Tuple[str, str, str, str, str]]) -> int:
    """
    FUNCTION    : insert_events
    DESCRIPTION : Inserts many rows into the events table.
    PARAMETERS  : rows - list of tuples in this order:
                 (event_ts, user_id, feature, event_type, session_id)
    RETURNS     : int - number of rows inserted
    """
    cursor = conn.cursor()

    # Using parameterized query to prevent SQL injection and ensure proper data handling
    cursor.executemany(
        """
        INSERT INTO events (event_ts, user_id, feature, event_type, session_id)
        VALUES (?, ?, ?, ?, ?);
        """,
        rows,
    )

    conn.commit()
    return cursor.rowcount
