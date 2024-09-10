import streamlit as st

from gpt.retriever import get_document_retriever, get_website_retriever


@st.cache_resource(show_spinner="Embedding file...")
def get_cached_document_retriever(input_file, api_key):
    return get_document_retriever(input_file, api_key)


@st.cache_resource(show_spinner="Loading Url...")
def get_cached_website_retriever(input_url, api_key):
    return get_website_retriever(input_url, api_key)
