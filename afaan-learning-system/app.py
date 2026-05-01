import streamlit as st
from db import init_db
from logic import load_vocab, get_random_question, check_answer
import sqlite3

# Setup database
init_db()

st.title("Afaan Oromo Learning App")

df = load_vocab()
if "current_question" not in st.session_state:
  st.session_state.current_question = get_random_question(df)

question = st.session_state.current_question

st.subheader(f"What is the meaning of: {question['oromo']}")

user_answer = st.text_input("Your answer:")

if st.button("Submit"):
  correct = check_answer(question['english'], user_answer)

  st.write("✅ Correct!" if correct else f"❌ Wrong. Correct answer: {question['english']}")

  conn = sqlite3.connect("database.sqlite")
  cursor = conn.cursor()

  cursor.execute("""
      INSERT INTO attempts (word_id, user_answer, correct)
      VALUES (?, ?, ?)
  """, (question["id"], user_answer, int(correct)))

  conn.commit()
  conn.close()

# Get the next question
st.session_state.current_question = get_random_question(df)
