from kafka import KafkaConsumer
import json

# Kafka Consumer 설정
consumer = KafkaConsumer(
    'analyze-result',                      # ✅ 결과 토픽 이름
    bootstrap_servers=['localhost:9092'],  # Kafka 브로커 주소
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='result-viewer'
)

print("🔍 analyze-result 토픽에서 GPT 요약 결과 수신 대기 중...\n")

# 메시지 수신 루프
for message in consumer:
    result = message.value
    print("🟢 결과 수신됨!")
    print(f"📦 ID: {result.get('id')}")
    print(f"🧠 요약 결과:\n{result.get('summary')}\n")
