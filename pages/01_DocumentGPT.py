import streamlit as st

from session.service import save_message_on_session,initial_message_on_session
from gpt.chain import create_chain
from view.cache import get_cached_retriever
from view.message import print_message, paint_history


st.set_page_config(
    page_title="DocumentGPT",
    page_icon="📃",
)

st.title("DocumentGPT")

st.markdown(
    """
    어서오세요.

    문서 파일을 읽고 질문에 대한 답을 해드립니다.
    좌측의 사이드바에서 OpenAI API 키를 입력해주세요
    """
)

with st.sidebar:
    api_key = st.text_input("OpenAI API 키를 입력해주세요.")
    st.write(f"API 키 : {api_key}")

    if(api_key):
        input_file = st.file_uploader(
            "문서 파일을 선택 해주세요. (.txt, .pdf, .docx)",
            type=["pdf", "txt", "docx"],
        )

if api_key and input_file:
    retriever = get_cached_retriever(input_file, api_key)

    print_message("안녕하세요. 어떤 것이 알고싶나요?", "ai")
    paint_history()

    input_message = st.chat_input("선택한 문서 파일에 대한 질문을 해주세요.")
    if input_message:
        print_message(input_message, "human")
        save_message_on_session(input_message,"human")

        chain = create_chain(retriever, api_key)
        with st.chat_message("ai"):
            chain.invoke(input_message)
else:
    initial_message_on_session()

if not api_key:
    st.warning("OpenAI API키를 입력해주세요.")
elif not input_file:
    st.info("파일을 선택해주세요.")