from pathlib import Path

TOTAL_QUESTIONS = 10

# Anchor paths to file locations
"""
On the terminal, the app will be run in afaan_learning_system:

streamlit run app.py
"""
BASE_DIR = Path(__file__).resolve().parent.parent # afaan_learning_system
DATA_DIR = BASE_DIR / "data"

DB_PATH = DATA_DIR / "database.sqlite"
VOCAB_PATH = DATA_DIR / "vocab.csv"
SCHEMA_PATH = DATA_DIR / "schema.sql"
