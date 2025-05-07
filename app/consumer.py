from kafka import KafkaConsumer
import json
from app.config import KAFKA_BROKER, REQUEST_TOPIC
from app.gpt import summarize_with_gpt
from app.producer import send_summary

consumer = KafkaConsumer(
    REQUEST_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def listen_and_process():
    for message in consumer:
        data = message.value
        comments = data.get('comments', [])
        summary = summarize_with_gpt(comments)
        send_summary(data['id'], summary)
