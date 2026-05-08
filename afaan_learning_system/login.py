# Login page
import streamlit as st
from core.config import BASE_DIR

def show_login() -> str:
  st.title("Login")

  username = st.text_input("Enter username", autocomplete="off")

  if st.button("Create my account"):
    if username.strip():
      st.session_state.logged_in = True
      st.session_state.username = username.strip()
      st.rerun()
    else:
      st.error("Please enter a username")
    



