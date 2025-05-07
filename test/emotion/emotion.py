# ===== 감정분석만 수행 (Hugging Face 기반, JSON → Elasticsearch 저장) =====
import json
import logging
from datetime import datetime
from transformers import pipeline
from elasticsearch import Elasticsearch

# Logging 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuggingFaceSentimentAnalyzer:
    def __init__(self):
        # Hugging Face pipeline 로드
        self.sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

    def analyze_sentiment(self, text):
        try:
            results = self.sentiment_pipeline(text)
            result = results[0]
            label = result['label']
            score = result['score']

            if '1' in label or '2' in label:
                sentiment = "negative"
            elif '3' in label:
                sentiment = "neutral"
            else:
                sentiment = "positive"
        except Exception as e:
            logger.error(f"Hugging Face 감정 분석 실패: {e}")
            sentiment = "neutral"
            score = 0.0

        return {
            "sentiment": sentiment,
            "confidence": round(score, 3)
        }

def analyze_from_json(json_path, es_index="youtube_sentiment", es_host="http://localhost:9200"):
    # Elasticsearch 연결
    es = Elasticsearch(es_host)
    if not es.ping():
        logger.error("❌ Elasticsearch 연결 실패")
        return

    analyzer = HuggingFaceSentimentAnalyzer()

    with open(json_path, "r", encoding="utf-8") as f:
        comments = json.load(f)

    for comment in comments:
        if "reply" not in comment:
            logger.warning("⚠️ 'reply' 필드 없음: %s", comment)
            continue

        reply_text = comment["reply"]
        logger.info("💬 감정 분석 중: %s", reply_text)

        sentiment_result = analyzer.analyze_sentiment(reply_text)

        doc = {
            "original": comment,
            "sentiment": sentiment_result,
            "analyzed_at": datetime.utcnow().isoformat()
        }

        try:
            es.index(index=es_index, document=doc)
            logger.info("✅ Elasticsearch 저장 완료: %s", doc)
        except Exception as e:
            logger.error("❌ Elasticsearch 저장 실패: %s", e)

if __name__ == "__main__":
    
    json_file_path = "re_clean.json"  
    # analyze_from_json(json_file_path)
