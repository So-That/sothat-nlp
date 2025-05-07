from transformers import pipeline, XLMRobertaTokenizer, XLMRobertaForSequenceClassification
import json
from pathlib import Path

# 모델명 지정
model_name = "joeddav/xlm-roberta-large-xnli"

# 모델 및 토크나이저 로드
tokenizer = XLMRobertaTokenizer.from_pretrained(model_name)
model = XLMRobertaForSequenceClassification.from_pretrained(model_name)

# 분류 파이프라인 생성
classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)

# 제품 리뷰에 적합한 라벨들
labels = [
    "가격", "성능", "디자인", "사용성", "기능",
    "구매결정", "고객서비스", "기타"
]

# 데이터 로드
with open("data/bertopic_topic.json", "r", encoding="utf-8") as f:
    topic_data = json.load(f)
sentences = topic_data["topic_0"]

# 분류 결과 저장
categorized = []
for i, sentence in enumerate(sentences):
    result = classifier(sentence, labels, multi_label=True)
    entry = {
        "index": i,
        "text": sentence,
        "labels": [
            {"label": label, "score": float(score)}
            for label, score in zip(result["labels"], result["scores"])
            if score > 0.3  # 기준점: 0.3 이상만 채택
        ]
    }
    categorized.append(entry)

# 결과 저장
output_file = "data/categorized_general_product_reviews.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(categorized, f, ensure_ascii=False, indent=2)

print(f"✅ 저장 완료: {output_file}")
