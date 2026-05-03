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

  st.session_state.feedback = (
    "✅ Correct!" if correct else f"❌ Wrong. Correct answer: {q['english']}"
  )
  
  st.session_state.correct = correct

  # Write user performance to database.sqlite
  # Records answer and whether or not answer was correct

  conn = sqlite3.connect("database.sqlite")
  cursor = conn.cursor()

  cursor.execute("""
      INSERT INTO attempts (word_id, user_answer, correct)
      VALUES (?, ?, ?)
  """, (q["id"], user_answer, int(correct)))

  conn.commit()
  conn.close()

  # Reset input 
  st.session_state['user_answer'] = ""

def next_question():
  st.session_state['current_question'] = get_random_question(df) # retrieve another random word
  st.session_state.feedback = ""
  st.session_state.correct = False
  st.session_state.user_answer = ""

# -----------------------
# UI layout
# -----------------------
st.subheader(f"What is the meaning of: {q['oromo']}")

user_answer = st.text_input(
  "Your answer:", 
  key="user_answer", 
  autocomplete="off"
)

col1, col2 = st.columns([3,1])

with col1:
  if not st.session_state.correct:
    st.button("Submit", on_click=submit)

with col2:
  st.button("Next Question", on_click=next_question)

# -----------------------
# Feedback display
# -----------------------
if st.session_state.feedback:
    st.info(st.session_state.feedback)
  






