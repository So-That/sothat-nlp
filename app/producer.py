from kafka import KafkaProducer
import json
from app.config import KAFKA_BROKER, RESPONSE_TOPIC

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

def send_summary(request_id, summary_text):
    message = {
        "id": request_id,
        "summary": summary_text
    }
    producer.send(RESPONSE_TOPIC, message)
