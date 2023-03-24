import logging
import requests

from google.cloud import vision
from app.config.constants import slack_token


def text_detection(files: list):
    result = []

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    for file in files:
        url = file.get("url_private_download")
        logging.info(f"url: {url}")
        response = requests.get(url, headers={"Authorization": f"Bearer {slack_token}"})

        image = vision.Image(content=response.content)

        # Performs label detection on the image file
        response = client.text_detection(image=image)
        texts = response.text_annotations
        result.append("\n".join([text.description for text in texts]))
    return result