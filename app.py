import streamlit as st

from session.service import save_message_on_session,initial_message_on_session
from gpt.chain import create_chain
from view.cache import get_cached_retriever
from view.message import print_message, paint_history


st.set_page_config(
    page_title="FullstackGPT Home",
    page_icon="🤖",
)

st.title("FullstackGPT")

st.markdown(
    """
    원하는 기능을 선택해주세요.

    - [DocumentGPT](/DocumentGPT) : 문서 파일을 읽고 질문에 대한 답을 해드립니다.
    - [QuizGPT](/QuizGPT)
    """
)
