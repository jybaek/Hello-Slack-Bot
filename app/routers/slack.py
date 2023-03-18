import logging

import requests
from fastapi import APIRouter
from slack_sdk import WebClient
from starlette.background import BackgroundTasks
from starlette.responses import Response

from app.config.constants import openai_token, url, slack_token, channel

router = APIRouter()


def write_notification(message: dict):
    logging.info(f"message: {message}")

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": openai_token,
    }

    # Set the data to send
    event = message.get("event")
    params = {"model": "gpt-3.5-turbo", "user_id": event.get("user")}
    content = "".join(event.get("text").split("> ")[1:])
    data = {"role": "user", "content": content}

    # Send messages to the ChatGPT server and respond to Slack
    response = requests.post(url, headers=headers, json=data, params=params)
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
