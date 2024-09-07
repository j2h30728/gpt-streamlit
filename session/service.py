
import streamlit as st


def save_message_on_session(message, role):
    st.session_state["messages"].append({"message": message, "role": role})

def initial_message_on_session():
    st.session_state["messages"] = []
