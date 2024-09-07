import streamlit as st

from gpt.retriever import get_retriever


@st.cache_resource(show_spinner="Embedding file...")
def get_cached_retriever(input_file, api_key):
    return get_retriever(input_file, api_key)
