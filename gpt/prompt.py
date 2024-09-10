from langchain.prompts import ChatPromptTemplate


STUFF_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Answer the question using ONLY the following context. If you don't know the answer just say you don't know. DON'T make anything up.
            
            Context: {context}
            """,
        ),
        ("human", "{question}"),
    ]
)


SITEMAP_ANSWER_PROMPT = ChatPromptTemplate.from_template(
    """
    주어진 context만을 사용하여 사용자의 질문에 답변하세요. 답변할 수 없는 경우, '모른다'고 말하고 절대 추측하지 마세요.
                                                  
    그런 다음 답변에 0점에서 5점 사이의 점수를 부여하세요. 답변이 사용자의 질문을 정확히 답하면 점수가 높아야 하고, 그렇지 않으면 낮아야 합니다.
    점수가 0점일지라도 항상 점수를 포함해야 합니다.
    Context: {context}
                                                  
    예시:
                                                  
    질문: 달까지의 거리는 얼마나 되나요?
    답변: 달은 384,400km 떨어져 있습니다.
    점수: 5
                                                  
    질문: 태양까지의 거리는 얼마나 되나요?
    답변: 잘 모르겠습니다.
    점수: 0
                                                  
    이제 당신의 차례입니다!
    질문: {question}
    """
)


SITEMAP_CHOOSE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            사용자 질문에 대답하기 위해 반드시 아래의 미리 제공된 답변만을 사용하세요.
            가장 점수가 높은 (더 유용한) 답변을 사용하고, 최신 답변을 우선적으로 선택하세요.
            출처를 반드시 인용하고, 답변에 포함된 출처는 변경하지 말고 그대로 반환하세요.
            답변들: {answers}
            """,
        ),
        ("human", "{question}"),
    ]
)
