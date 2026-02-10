"""
FILE          : load_data_for_charts.py
PROJECT       : User-Activity-Analytics-Reporting-System
DESCRIPTION   :
    One-time setup script:
    - Creates the SQLite table 'events' if it doesn't exist
    - Loads data from a CSV file into the 'events' table
"""

from src.db import connect_db, init_db, insert_events
from src.ingest import read_and_clean_csv


def main() -> None:
    # 1) Where your CSV data is
    csv_path = "data/sample_activity.csv"

    # 2) Where your SQLite database file is
    db_path = "data/activity.db"

    # 3) Read + clean the CSV into a DataFrame (table in Python)
    df = read_and_clean_csv(csv_path)

    # 4) Open the database and create the events table if missing
    conn = connect_db(db_path)
    init_db(conn)

    # 5) Convert the DataFrame into a list of tuples for insert_events()
    rows = list(
        zip(
            df["event_ts"].tolist(),
            df["user_id"].tolist(),
            df["feature"].tolist(),
            df["event_type"].tolist(),
            df["session_id"].tolist(),
        )
    )

    # 6) Insert rows into the database
    inserted = insert_events(conn, rows)
    conn.close()

    print("OK: Database initialized and data inserted.")
    print("Inserted rows:", inserted)
    print("DB path:", db_path)


if __name__ == "__main__":
    main()
