[![Python 3.x](https://img.shields.io/badge/python-3.x-green.svg)](https://www.python.org/downloads/release/python-360/)

# ChatGPT API with FastAPI
A server for handling Slack Event Subscriptions. It communicates with the ChatGPT API server.

## Prerequisite
- Docker

Before running the application, make sure that Docker is installed and running on your system.

Very important: Set and use all the environment variables in [app/config/constants.py](app/config/constants.py).

## Local Execution Guide
1. First, to run this application in your local environment, please execute the following command to install the required libraries.
```bash
pip install -r requirements.txt
```

2. Once the necessary libraries have been installed, execute the following command to run the application.
```bash
uvicorn app.main:app --reload
```
This command will run the application based on the app object in the main module of the app package. 
You can use the --reload option to automatically reload the application when file changes are detected.

## Installation
1. Clone the repository:
```bash
https://github.com/jybaek/Hello-Slack-Bot.git
cd Hello-Slack-Bot
```

2. Build the Docker image:
```bash
docker build -t slack-bot .
```

3. Run the Docker container:
```bash
docker run --rm -it -p8000:8000 slack-bot
```

4. Open your web browser and go to `http://localhost:8000/docs` to access the Swagger UI and test the API.

## API Documentation
The API documentation can be found at `http://localhost:8000/docs` once the Docker container is running.

## Usage
If you want to send a message from Swagger, [here's](https://api.slack.com/apis/connections/events-api#events-JSON) a link.



## License
This project is licensed under the terms of the MIT license. See [LICENSE](license) for more information.
