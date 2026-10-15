import sqlite3
from core.config import BASE_DIR, SCHEMA_PATH

def get_connection():
  db_path = BASE_DIR / "data" / "database.sqlite"
  return sqlite3.connect(db_path)

def init_db():
  """Create the application tables and add quiz_id to existing attempts tables."""
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

  cursor.execute("PRAGMA table_info(attempts)")
  columns = {row[1] for row in cursor.fetchall()}

  if 'quiz_id' not in columns:
    cursor.execute("ALTER TABLE attempts ADD COLUMN quiz_id TEXT")

  conn.commit()
  conn.close()


def get_correct_count(quiz_id: str) -> int:
  """Return the number of correct answers recorded for one quiz."""
  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute("""
  SELECT COALESCE(SUM(correct), 0)
  FROM attempts
  WHERE quiz_id = ?
  """, (quiz_id,))

  result = cursor.fetchone()[0]

  conn.close()
  return result