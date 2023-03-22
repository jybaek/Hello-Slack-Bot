import os

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))

slack_token = os.environ.get("slack_token")
openai_token = os.environ.get("openai_token")
chat_server_url = os.environ.get("chat_server")
number_of_messages_to_keep = int(os.environ.get("number_of_messages_to_keep", "0"))
