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

q = st.session_state.current_question

# -----------------------
# UI layout
# -----------------------
st.subheader(f"What is the meaning of: {q['oromo']}")

user_answer = st.text_input("Your answer:", key="user_answer", autocomplete="off")

# -----------------------
# Submit logic
# -----------------------

# Check user answer after they press the submit button
def submit():
  answer = st.session_state.user_answer.strip()
  
  correct = check_answer(q['english'], answer)

  st.session_state.feedback = (
    st.write("✅ Correct!" if correct else f"❌ Wrong. Correct answer: {q['english']}")
  )
  
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
  st.session_state['current_question'] = get_random_question(df)
  st.session_state.feedback = ""

st.button("Submit",on_click=submit)
st.button("Next Question", on_click=next_question)
