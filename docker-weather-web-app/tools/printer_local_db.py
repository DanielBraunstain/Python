import sqlite3
from setup import get_db_path

def print_sqlite_file():
    """
    prints data in sqlite file weather.db
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM daily_summaries")
    for row in cursor.fetchall():
        print(row)

    conn.close()


if __name__ == "__main__":
    print_sqlite_file()

