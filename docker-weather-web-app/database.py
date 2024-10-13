import sqlite3
from setup import get_db_path

def init_db():
    """
    initialize SQLite db file.
    """
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS daily_summaries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        location TEXT NOT NULL,
                        date TEXT NOT NULL,
                        temp_mor REAL,
                        temp_eve REAL,
                        humidity_mor REAL,
                        humidity_eve REAL
                    )''')
    conn.commit()
    conn.close()

def store_daily_summaries(db, location, summaries):
    """
    store filtered summaries data in the appropriate database.
    """
    if isinstance(db, str):  # SQLite
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        for summary in summaries:
            cursor.execute('''INSERT INTO daily_summaries (location, date, temp_mor, temp_eve, humidity_mor, humidity_eve)
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (location, summary['date'], summary['temp_mor'], summary['temp_eve'],
                            summary['humidity_mor'], summary['humidity_eve']))
        conn.commit()
        conn.close()
    else:  # MongoDB
        collection = db.db.daily_summaries
        for summary in summaries:
            summary['location'] = location
            collection.insert_one(summary)
