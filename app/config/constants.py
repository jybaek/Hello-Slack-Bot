import os

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))

slack_token = os.environ.get("slack_token")
channel = os.environ.get("channel")
openai_token = os.environ.get("openai_token")
url = os.environ.get("chat_server")
