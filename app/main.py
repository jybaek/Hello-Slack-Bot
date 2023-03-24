import logging

import uvicorn
from fastapi import FastAPI
from starlette.responses import Response
from .routers import slack

app = FastAPI()
app.include_router(slack.router)

logging.basicConfig(level=logging.INFO)


@app.get("/")
async def root():
    return Response("Hello Slack Applications!")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        access_log=False,
        reload=True,
        timeout_keep_alive=65,
    )
