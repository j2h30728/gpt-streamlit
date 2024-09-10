import streamlit as st

from session.service import save_message_on_session,initial_message_on_session
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
    - [SiteGPT](/SiteGPT) : 웹페이지를 읽고 질문에 대한 답을 해드립니다.
    """
)

with st.sidebar:
    api_key = st.session_state.get("api_key", None)
    if not api_key:
        api_key = st.text_input("OpenAI API 키를 입력해주세요.")
        st.session_state["api_key"] = api_key

    st.write(f"API 키 : {api_key}")
