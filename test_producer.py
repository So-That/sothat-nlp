from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

message = {
    "id": "test-001",
    "comments": [
        "정말 만족스러워요!",
        "화면이 밝고 선명합니다.",
        "배터리만 좀 더 오래 갔으면 좋겠네요."
    ]
}

producer.send('analyze-request', message)
producer.flush()
print("✅ 테스트 댓글 메시지 전송 완료")
