import streamlit as st
from core.db import init_db, get_connection
from core.logic import load_vocab, get_random_question, check_answer
from core.config import TOTAL_QUESTIONS

# -----------------------
# Setup
# -----------------------
init_db()

st.title("Proficiency Test")

df = load_vocab()

# -----------------------
# Session state setup
# -----------------------
if "current_question" not in st.session_state:
  st.session_state.current_question = get_random_question(df)

# Response for user answer
if "feedback" not in st.session_state:
  st.session_state.feedback = ""

# Boolean state to handle responses for correct answers
if "correct" not in st.session_state:
  st.session_state.correct = False
  
if "question_count" not in st.session_state:
  st.session_state.question_count = 0

q = st.session_state.current_question

# Go to the results page if all 10 questions are answered
if st.session_state.question_count == TOTAL_QUESTIONS:
  st.switch_page("pages/result.py")
  st.session_state.question_count = 0
  st.session_state.feedback = ""

# -----------------------
# Submit logic
# -----------------------

# Events after user submits answer
def submit():
  q = st.session_state.current_question
  user_answer = st.session_state.user_answer.strip()

  correct = check_answer(q['english'], user_answer)
  
  st.session_state.correct = correct

  # Write user performance to database.sqlite
  # Records answer and whether or not answer was correct

  conn = get_connection()
  cursor = conn.cursor()

  cursor.execute("""
      INSERT INTO attempts (word_id, user_answer, correct)
      VALUES (?, ?, ?)
  """, (q["id"], user_answer, int(correct)))

  conn.commit()
  conn.close()

  st.session_state['current_question'] = get_random_question(df) # retrieve another random word

  st.session_state.feedback = (
    "✅ Correct!" if correct else f"❌ Wrong. Correct answer: {q['english']}"
  )

  # Reset input 
  st.session_state['user_answer'] = ""

  # Increment question count
  st.session_state.question_count += 1

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
  st.session_state.feedback = ""
  
# Progress bar
st.progress(st.session_state.question_count / TOTAL_QUESTIONS)





