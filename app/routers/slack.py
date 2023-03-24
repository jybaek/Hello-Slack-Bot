import logging

import requests
from fastapi import APIRouter
from slack_sdk import WebClient
from starlette.background import BackgroundTasks
from starlette.responses import Response

from app.config.constants import openai_token, chat_server_url, slack_token, number_of_messages_to_keep
from app.google.vision import text_detection, localize_objects

router = APIRouter()


def write_notification(message: dict):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": openai_token,
    }

    # Set the data to send
    event = message.get("event")
    channel = event.get("channel")
    thread_ts = event.get("thread_ts") if event.get("thread_ts") else event.get("ts")

    # Image processing
    texts_in_images, object_in_image = [], []
    system_message = ""
    if files := event.get("files"):
        texts_in_image = text_detection(files)
        object_in_image = localize_objects(files)
        system_message = "\n".join(
            [
                f"{index} 번째 사진에는 다음과 같은 글자와 객체가 있어. {text}, {object_}."
                for index, (text, object_) in enumerate(zip(texts_in_image, object_in_image), 1)
            ]
        )
        system_message += "이제 이 사진에 대해서 질문 할 거야. "

    params = {
        "model": "gpt-3.5-turbo",
        "context_unit": thread_ts,
        "number_of_messages_to_keep": number_of_messages_to_keep,
    }
    content = "".join(event.get("text").split("> ")[1:])
    data = {"role": "user", "content": system_message + content}

    logging.info(f"message: {data}")

    # Send messages to the ChatGPT server and respond to Slack
    response = requests.post(chat_server_url, headers=headers, json=data, params=params)
    response.encoding = "utf-8"
    logging.info(response.text)
    client = WebClient(token=slack_token)
    client.chat_postMessage(
        channel=channel, text=response.text, thread_ts=event.get("ts") if event.get("ts") else event.get("thread_ts")
    )


@router.post("/chat")
async def root(message: dict, background_tasks: BackgroundTasks):
    if message.get("challenge"):
        return message.get("challenge")

    # Because Slack is constrained to give a response in 3 seconds, ChatGPT processing is handled by background_tasks.
    background_tasks.add_task(write_notification, message)

    logging.info("response ok")
    return Response("ok")
