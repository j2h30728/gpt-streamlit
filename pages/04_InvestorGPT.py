
import streamlit as st

from gpt.model import create_default_chat_open_model
from view.cache import get_cached_website_retriever
from view.message import print_message, paint_history
from session.service import initial_message_on_session


st.set_page_config(
    page_title="InvestorGPT",
    page_icon="💼",
)

st.markdown(
    """
    # InvestorGPT
            
    InvestorGPT에 오신 것을 환영합니다.
            
    관심 있는 회사의 이름을 입력하세요. 에이전트가 조사를 해드립니다.
"""
)

# session_state에서 API 키와 파일을 가져옴
api_key = st.session_state.get("api_key", None)
with st.sidebar:
    if not api_key:
        api_key = st.text_input("OpenAI API 키를 입력해주세요.")
        st.session_state["api_key"] = api_key
    
    if api_key:
        llm = create_default_chat_open_model(api_key)
        input_query = st.text_input(
        "검색할 회사의 이름을 입력해주세요.",
        placeholder="Apple",
    )


if api_key and input_query:
    if ".xml" not in input_query:
        with st.sidebar:
            st.error("검색할 회사의 이름을 입력해주세요.")
    else:
        retriever = get_cached_website_retriever(input_query, api_key)

        print_message("안녕하세요. 어떤 것이 알고싶나요?", "ai")
        paint_history()


else:
    initial_message_on_session()


if not api_key:
    st.warning("OpenAI API키를 입력해주세요.")
elif not input_query:
    st.info("검색할 회사의 이름을 입력해주세요.")
