import streamlit as st

def print_message(message, role):
    with st.chat_message(role):
        st.markdown(message)

def paint_history():
    for message in st.session_state["messages"]:
        print_message(
            message["message"],
            message["role"],
        )

