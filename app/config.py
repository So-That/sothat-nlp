import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
REQUEST_TOPIC = os.getenv("REQUEST_TOPIC")
RESPONSE_TOPIC = os.getenv("RESPONSE_TOPIC")
