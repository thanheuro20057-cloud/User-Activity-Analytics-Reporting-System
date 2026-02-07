import pandas as pd

REQUIRED_COLUMNS = {"event_ts", "user_id", "feature", "event_type", "session_id"}

def read_and_clean_csv(csv_path: str) -> pd.DataFrame:
    """
    Reads user activity CSV, validates required columns, cleans data,
    and returns a cleaned DataFrame ready for database insertion.
    """
    df = pd.read_csv(csv_path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing required columns: {sorted(missing)}")

    df = df.copy()

    df["event_ts"] = pd.to_datetime(df["event_ts"], errors="coerce")
    df = df.dropna(subset=["event_ts", "user_id", "feature", "event_type"])

    df["user_id"] = df["user_id"].astype(str).str.strip()
    df["feature"] = df["feature"].astype(str).str.strip().str.lower()
    df["event_type"] = df["event_type"].astype(str).str.strip().str.lower()
    df["session_id"] = df["session_id"].astype(str).str.strip()

    df["event_ts"] = df["event_ts"].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df.reset_index(drop=True)
