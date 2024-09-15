
import streamlit as st

from gpt.model import create_default_chat_open_model
from assistant.run import paint_download_btn
from assistant.client import get_assistant, create_OpenAI_model
from assistant.run import  send_thread_message, get_thread_messages, get_thread_id

st.set_page_config(
    page_title="OpenAI Assistants",
    page_icon="💼",
)

st.markdown(
    """
    # OpenAI Assistants 
            
    OpenAI Assistants 에 오신 것을 환영합니다.
            
    궁금한 단어를 입력하세요. 에이전트가 답변 해드립니다.
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
  
        
    st.markdown("---")
    st.write("https://github.com/j2h30728/gpt-streamlit.git")


if not api_key:
    st.error("OpenAI API키를 입력해주세요.")
else:
    query = st.chat_input("질문을 작성해주세요.")
    client = create_OpenAI_model(api_key)
    assistant_id = get_assistant(client).id

    # 메시지 기록 출력
    for idx, message in enumerate(get_thread_messages(client, get_thread_id(client))):
        with st.chat_message(message.role):
            st.markdown(message.content[0].text.value)
        if message.role == "assistant" and idx > 0:
            paint_download_btn(
                message.content[0].text.value, createdAt=message.created_at
            )

    if query:
        with st.chat_message("user"):
            st.markdown(query)
        send_thread_message(client, query)

