from langchain.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from bs4 import BeautifulSoup
import requests
import streamlit as st
from httpx import HTTPError
from tenacity import retry, stop_after_attempt, wait_exponential

from openai import OpenAI


from session.service import get_assistant_on_session, save_assistant_on_session

def create_OpenAI_model(api_key):
    client = OpenAI(api_key=api_key)
    return client


def get_assistant(client):
    if "assistant" in st.session_state:
        return get_assistant_on_session()
    assistant = createAssistant(client)
    save_assistant_on_session(assistant)

    return get_assistant_on_session()


def createAssistant(client):
  assistant = client.beta.assistants.create(
    name="검색 도우미", 
    instructions="""
    당신의 임무는 Wikipedia 또는 DuckDuckGo를 사용하여 제공된 쿼리에 대해 정보를 수집하는 것입니다.
    DuckDuckGo에서 관련 웹사이트를 찾았을 경우, 해당 웹사이트의 내용을 스크랩해야 합니다. 스크랩한 내용을 활용하여 질문에 대한 상세한 답변을 작성하세요.
    Wikipedia, DuckDuckGo 검색 결과, 그리고 찾은 관련 웹사이트에서 정보를 조합해 최종 답변을 완성하세요. 
    최종 답변은 체계적이고 상세해야 하며, 사용된 모든 출처에 대한 링크(출처 URL)를 포함해야 합니다.
    검색 결과는 .txt 파일로 저장할 수 있어야 하며, 파일의 내용은 제공된 상세 결과와 일치해야 합니다. 모든 출처와 관련 정보를 반드시 포함하세요.
    Wikipedia에서 찾은 정보는 반드시 포함해야 합니다.
    """, 
    model="gpt-4o-mini",
    temperature=0.1,
    tools=functions_call
  )
  return assistant



functions_call = [
    {
        "type": "function",
        "function": {
            "name": "get_ddg_results",
            "description": "DuckDuckGo 검색 엔진을 사용하여 query 검색을 진행합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "검색에 필요한 query",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_wiki_results",
            "description": "wikipedia에서 query 검색을 진행합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "검색에 필요한 query",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_web_content",
            "description": "DuckDuckGo에서 찾은 웹 사이트 링크를 통해 검색을 진행합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "스크랩할 웹페이지의 URL",
                    },
                },
                "required": ["url"],
            },
        },
    },
]


def get_ddg_results(inputs):
    query = inputs["query"]
    search = DuckDuckGoSearchAPIWrapper()
    try:
        return search.run(query)
    except HTTPError as e:
        print(f"DuckDuckGo 검색 중 오류 발생: {e}")
        return f"DuckDuckGo 검색 중 오류가 발생했습니다: {str(e)}. 다른 검색 방법을 시도해보세요."

def get_wiki_results(inputs):
    query = inputs["query"]
    wrapper = WikipediaAPIWrapper()
    wiki = WikipediaQueryRun(api_wrapper=wrapper)
    return wiki.run(query)


def get_web_content(inputs):
    url = inputs["url"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        for header in soup.find_all(["header", "footer", "nav"]):
            header.decompose()
        content = soup.get_text(separator="\n", strip=True)

        return content

    except requests.RequestException as e:
        print(f"get_web_content 오류 : {e}")
        return f"{url} 링크에서 오류가 발생했습니다. 다른 url을 사용해주세요."
    

functions_map = {
    "get_ddg_results": get_ddg_results,
    "get_web_content": get_web_content,
    "get_wiki_results": get_wiki_results,
}