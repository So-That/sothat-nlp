from kafka import KafkaConsumer, KafkaProducer
import openai
import json
import os
from dotenv import load_dotenv

# 환경 변수 로드 (.env에 OPENAI_API_KEY 저장)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Kafka 설정
KAFKA_BROKER = 'localhost:9092'
CONSUMER_TOPIC = 'gpt'
PRODUCER_TOPIC = 'report'
GROUP_ID = 'gpt_group'

# Kafka Consumer
consumer = KafkaConsumer(
    CONSUMER_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=GROUP_ID
)

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

def call_gpt(prompt: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 댓글을 요약하는 AI입니다."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.7
    )
    return response.choices[0].message.content

def process_message(data):
    video_id = data.get("id")
    cluster = data.get("cluster", "기타")
    comments = data.get("comments", [])

    print(f"📥 수신: id={video_id}, cluster={cluster}, 댓글 {len(comments)}개")

    if not comments:
        print("⚠️ 댓글 없음, 건너뜀")
        return

    prompt = f"다음은 '{cluster}'에 대한 유튜브 댓글입니다:\n" + "\n".join(comments) + "\n\n요약해줘."
    try:
        summary = call_gpt(prompt)
        print(f"🧠 GPT 요약 완료:\n{summary[:100]}...")

        result = {
            "id": video_id,
            "cluster": cluster,
            "summary": summary
        }

        producer.send(PRODUCER_TOPIC, result)
        print("✅ 결과 전송 완료\n")

    except Exception as e:
        print(f"❌ GPT 호출 실패: {e}")

if __name__ == "__main__":
    print("🚀 GPT 컨슈머 시작됨 (토픽: gpt, 그룹: gpt_group)...\n")
    for message in consumer:
        process_message(message.value)
