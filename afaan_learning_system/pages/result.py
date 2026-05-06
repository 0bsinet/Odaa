# Results for after the user completes their proficiency test
import streamlit as st
from core.config import TOTAL_QUESTIONS
from core.db import get_correct_count
from core.config import BASE_DIR

st.title("Results")

correct_answers = get_correct_count(TOTAL_QUESTIONS)

st.subheader(f"You scored {correct_answers} out of {TOTAL_QUESTIONS} right!")

if st.button("Try Again"):
  st.session_state.question_count = 0
  st.session_state.feedback = ""
  st.switch_page(BASE_DIR / "app.py")
  