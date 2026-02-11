from pathlib import Path
from Model.db import connect_db
from View.charts import generate_all_charts

def main() -> None:
    conn = connect_db("data/activity.db")
    paths = generate_all_charts(conn, Path("reports/assets"))
    conn.close()

    print("Charts created:")
    for p in paths:
        print("-", p)

if __name__ == "__main__":
    main()
