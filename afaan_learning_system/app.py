import streamlit as st
from login import show_login
from quiz import show_quiz
from home import show_home
from result import show_results

# Initialize login state
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False

if "page" not in st.session_state:
  st.session_state.page = "home"

# Handle page routing
if not st.session_state.logged_in:
  show_login()

else:
  if st.session_state.page == "home":
    show_home()
  
  if st.session_state.page == "result":
    show_results()
  
  elif st.session_state.page == "quiz":
    show_quiz()


