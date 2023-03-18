import logging

from fastapi import FastAPI
from starlette.responses import Response
from .routers import slack

app = FastAPI()
app.include_router(slack.router)

logging.basicConfig(level=logging.INFO)


@app.get("/")
async def root():
    return Response("Hello Slack Applications!")
