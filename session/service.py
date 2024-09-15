
import streamlit as st


def save_message_on_session(message, role):
    st.session_state["messages"].append({"message": message, "role": role})

def initial_message_on_session():
    st.session_state["messages"] = []


def save_assistant_on_session(assistant):
    st.session_state["assistant"] = assistant

def get_assistant_on_session():
    return st.session_state["assistant"]

def save_thread_id_on_session(thread_id):
    st.session_state['thread_id'] = thread_id

def get_thread_id_on_session():
    return st.session_state["thread_id"]

def save_run_on_session(run):
    st.session_state['run'] = run

def get_run_on_session():
    return st.session_state["run"]