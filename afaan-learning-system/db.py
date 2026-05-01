import sqlite3

def get_connection():
  return sqlite3.connect("database.sqlite")

def init_db():
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute("""
  CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_id INTEGER,
    user_answer TEXT,
    correct INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
  )
  """)

  conn.commit()
  conn.close()