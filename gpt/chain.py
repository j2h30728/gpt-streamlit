from langchain.schema.runnable import RunnableLambda, RunnablePassthrough

from gpt.model import create_chat_open_model
from gpt.prompt import DEFAULT_PROMPT

def create_chain(retriever, api_key):
    llm = create_chat_open_model(api_key)
    chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
            }
            | DEFAULT_PROMPT
            | llm
        )
    return chain
    

def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)
