# Homepage
import streamlit as st 

def show_home():
  if st.session_state.get("logged_in"):
    st.title(f"Welcome {st.session_state.username}!")
  else:
    st.warning("Please log in first.")

  st.subheader("My Activities:")
  
  if st.button("Practice Vocabulary"):
    st.session_state.page = "quiz"
    st.rerun()