from langchain.document_loaders import SitemapLoader
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings

import streamlit as st

from gpt.chain import create_sitemap_chain
from gpt.model import create_default_chat_open_model
from view.cache import get_cached_website_retriever
from view.message import print_message, paint_history
from session.service import save_message_on_session,initial_message_on_session


st.set_page_config(
    page_title="SiteGPT",
    page_icon="🖥️",
)

st.markdown(
    """
    # SiteGPT
            
    Ask questions about the content of a website.
            
    Start by writing the URL of the website on the sidebar.
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
        input_url = st.text_input(
        "Sitemap URL을 입력해주세요.",
        placeholder="https://example.com/sitemap.xml",
    )


if api_key and input_url:
    if ".xml" not in input_url:
        with st.sidebar:
            st.error("Sitemap URL을 입력해주세요.")
    else:
        retriever = get_cached_website_retriever(input_url, api_key)

        print_message("안녕하세요. 어떤 것이 알고싶나요?", "ai")
        paint_history()

        input_message =  st.chat_input("웹 페이지에 대한 질문을 해주세요.")
        if input_message:
            print_message(input_message, "human")
            save_message_on_session(input_message,"human")
            chain = create_sitemap_chain(retriever, llm)
            with st.spinner('답변 준비 중...'):
                result = chain.invoke(input_message)
                answer = result.content.replace("$", "\$")
                print_message(answer, "ai")
                save_message_on_session(answer,"ai")
else:
    initial_message_on_session()


if not api_key:
    st.warning("OpenAI API키를 입력해주세요.")
elif not input_url:
    st.info("url을 입력해주세요.")
