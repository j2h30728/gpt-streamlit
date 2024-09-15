from datetime import datetime, timedelta, timezone
import streamlit as st
import json

from session.service import get_run_on_session, save_run_on_session
from assistant.client import functions_map
from session.service import get_thread_id_on_session, save_thread_id_on_session, get_assistant_on_session


def run_process(client, thread_id, assistant_id, content):
    if "run" not in st.session_state or get_run_status(client, get_run_on_session().id, get_thread_id(client)) in (
        "expired",
        "completed",
    ):
        start_run(client, thread_id, assistant_id, content)
    else:
        print("already running")

    run = get_run_on_session()

    with st.status("진행 중..."):
        while get_run_status(client, run.id, get_thread_id(client)) == "requires_action":
            submit_tool_outputs(client, run.id, get_thread_id(client))

    print(f"done, {get_run_status(client, run.id, get_thread_id(client))}")
    final_message = get_thread_messages(client, get_thread_id(client))[-1]
    if get_run_status(client, run.id, get_thread_id(client)) == "completed":
        with st.chat_message(final_message.role):
            st.markdown(final_message.content[0].text.value)

        paint_download_btn(
            final_message.content[0].text.value, createdAt=final_message.created_at
        )
        print(final_message)
    elif get_run_status(client, run.id, get_thread_id(client)) == "failed":
        with st.chat_message("assistant"):
            st.markdown("죄송합니다. 검색에 실패하였습니다. 다시 시도해주세요.")


def paint_download_btn(content, createdAt):
    file_bytes = content.encode("utf-8")

    created_at_utc = datetime.fromtimestamp(createdAt, tz=timezone.utc)
    kst_timezone = timezone(timedelta(hours=9))
    created_at_kst = created_at_utc.astimezone(kst_timezone)
    formatted_date = created_at_kst.strftime("%y_%m_%d_%H%M_Answer")

    st.download_button(
        label="답변 다운로드 하기",
        data=file_bytes,
        file_name=f"{formatted_date}_{createdAt}.txt",
        mime="text/plain",
        key=createdAt,
    )


def get_run(client, run_id, thread_id):
    return client.beta.threads.runs.retrieve(
        run_id=run_id,
        thread_id=thread_id,
    )


def get_run_status(client, run_id, thread_id):
    return client.beta.threads.runs.retrieve(
        run_id=run_id,
        thread_id=thread_id,
    ).status


def start_run(client, thread_id, assistant_id, content):
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=content
    )
    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id,
)
    save_run_on_session(run)


def get_tool_outputs(client, run_id, thread_id):
    run = get_run(client, run_id, thread_id)
    outputs = []
    for action in run.required_action.submit_tool_outputs.tool_calls:
        action_id = action.id
        function = action.function
        print(f"Calling function: {function.name} with arg {function.arguments}")
        output = functions_map[function.name](json.loads(function.arguments))
        outputs.append(
            {
                "output": output,
                "tool_call_id": action_id,
            }
        )
    return outputs


def submit_tool_outputs(client, run_id, thread_id):
    outputs = get_tool_outputs(client, run_id, thread_id)
    return client.beta.threads.runs.submit_tool_outputs_and_poll(
        run_id=run_id, thread_id=thread_id, tool_outputs=outputs
    )


def create_thread(client):
    thread = client.beta.threads.create(
            messages=[
                {
                    "role": "assistant",
                    "content": "안녕하세요. 어떤 것을 도와드릴까요?",
                }
            ]
        )
    return thread

def get_thread_id(client):
    if "thread_id" not in st.session_state:
        thread = create_thread(client)
        save_thread_id_on_session(thread.id)
    return get_thread_id_on_session()


def get_thread_messages(client, thread_id):
    messages = list(
        client.beta.threads.messages.list(
            thread_id=thread_id,
        )
    )
    return list(reversed(messages))

def send_thread_message(client, _content):
    thread_id = get_thread_id(client)
    assistant = get_assistant_on_session()
    run_process(client, thread_id, assistant.id, _content)


