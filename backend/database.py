import sqlite3

conn = sqlite3.connect("uxvision.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_name TEXT,
    score INTEGER,
    suggestions TEXT,
    timestamp TEXT
)
""")

conn.commit()
conn.close()