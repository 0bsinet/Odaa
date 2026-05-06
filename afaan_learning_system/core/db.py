import sqlite3
from core.config import BASE_DIR, SCHEMA_PATH

def get_connection():
  db_path = BASE_DIR / "data" / "database.sqlite"
  return sqlite3.connect(db_path)

def init_db():
  conn = get_connection()
  cursor = conn.cursor()

  # create table using .sql file queries
  with open(SCHEMA_PATH) as f:
    cursor.executescript(f.read())
    
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


"""
Firstly retrieves the last N attempts of the user
where N will be equal to TOTAL_QUESTIONS

Then it adds up all the 1's from the correct answers,
returning the total number of correct attempts
"""
def get_correct_count(limit: int = 10):
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute("""
  SELECT sum(CORRECT)
  FROM (
      SELECT correct
      FROM attempts
      ORDER BY id DESC
      LIMIT ?
  )
  """, (limit,))

  result = cursor.fetchone()[0]

  conn.close()
  return result