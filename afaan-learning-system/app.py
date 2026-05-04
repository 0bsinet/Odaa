import streamlit as st
from db import init_db
from logic import load_vocab, get_random_question, check_answer
import sqlite3

# -----------------------
# Setup
# -----------------------
init_db()

st.title("Afaan Oromo Learning App")

df = load_vocab()

# -----------------------
# Session state setup
# -----------------------
if "current_question" not in st.session_state:
  st.session_state.current_question = get_random_question(df)

if "feedback" not in st.session_state:
  st.session_state.feedback = ""

if "correct" not in st.session_state:
  st.session_state.correct = False

q = st.session_state.current_question

# -----------------------
# Submit logic
# -----------------------

# Check user answer after they press the submit button
def submit():
  q = st.session_state.current_question
  user_answer = st.session_state.user_answer.strip()

  correct = check_answer(q['english'], user_answer)
  
  st.session_state.correct = correct

  # Write user performance to database.sqlite
  # Records answer and whether or not answer was correct

  conn = sqlite3.connect("database.sqlite")
  print(conn.execute("PRAGMA database_list;").fetchall())
  cursor = conn.cursor()

  # create table using .sql file queries
  with open("afaan-learning-system/data/schema.sql") as f:
    cursor.executescript(f.read())

  cursor.execute("""
      INSERT INTO attempts (word_id, user_answer, correct)
      VALUES (?, ?, ?)
  """, (q["id"], user_answer, int(correct)))

  # read attempts
  cursor.execute("SELECT * FROM attempts")
  for row in cursor.fetchall():
    print(row)

  conn.commit()
  conn.close()

  st.session_state['current_question'] = get_random_question(df) # retrieve another random word

  st.session_state.feedback = (
    "✅ Correct!" if correct else f"❌ Wrong. Correct answer: {q['english']}"
  )

  # Reset input 
  st.session_state['user_answer'] = ""

# -----------------------
# UI layout
# -----------------------
st.subheader(f"What is the meaning of: {q['oromo']}")

user_answer = st.text_input(
  "Your answer:", 
  key="user_answer", 
  autocomplete="off"
)

st.button("Submit", on_click=submit)

# -----------------------
# Feedback display
# -----------------------
if st.session_state.feedback:
  st.info(st.session_state.feedback)






