from langchain.schema.runnable import RunnableLambda, RunnablePassthrough

from gpt.model import create_chat_open_model
from gpt.prompt import STUFF_PROMPT, SITEMAP_ANSWER_PROMPT, SITEMAP_CHOOSE_PROMPT

def create_stuff_chain(retriever, api_key):
    llm = create_chat_open_model(api_key)
    chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
            }
            | STUFF_PROMPT
            | llm
        )
    return chain

def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


def create_sitemap_chain(retriever, llm):
     chain = (
                {
                    "docs": retriever,
                    "question": RunnablePassthrough(),
                }
                | RunnableLambda(lambda inputs : get_answers(inputs, llm))
                | RunnableLambda(lambda inputs : choose_answer(inputs, llm))
            )
     return chain
    
def create_sitemap_answer_chain(llm):
    chain = ( SITEMAP_ANSWER_PROMPT | llm )
    return chain
    
def create_sitemap_choose_chain(llm):
    chain = ( SITEMAP_CHOOSE_PROMPT | llm )
    return chain    


def get_answers(inputs,llm):
    docs = inputs["docs"]
    question = inputs["question"]
    answers_chain = create_sitemap_answer_chain(llm)
    return {
        "question": question,
        "answers": [
            {
                "answer": answers_chain.invoke(
                    {"question": question, "context": doc.page_content}
                ).content,
                "source": doc.metadata["source"],
                "date": doc.metadata["lastmod"],
            }
            for doc in docs
        ],
    }


def choose_answer(inputs,llm):
    answers = inputs["answers"]
    question = inputs["question"]
    choose_chain = create_sitemap_choose_chain(llm)
    condensed = "\n\n".join(
        f"{answer['answer']}\nSource:{answer['source']}\nDate:{answer['date']}\n"
        for answer in answers
    )
    return choose_chain.invoke(
        {
            "question": question,
            "answers": condensed,
        }
    )
