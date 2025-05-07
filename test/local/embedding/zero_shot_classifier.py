import json
from transformers import pipeline, XLMRobertaTokenizer, XLMRobertaForSequenceClassification

# ========================
# 1. 모델 세팅
# ========================
model_name = "joeddav/xlm-roberta-large-xnli"
tokenizer = XLMRobertaTokenizer.from_pretrained(model_name)
model = XLMRobertaForSequenceClassification.from_pretrained(model_name)
classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)

# ========================
# 2. 라벨 + 설명 세팅
# ========================
raw_labels = ["가격", "성능", "디자인", "기타"]

labels = [
    "가격 - 제품의 가격, 할인, 비용, 가성비에 대한 내용",
    "성능 - 냉장고의 기능, 성능, 품질에 대한 평가나 정보",
    "디자인 - 냉장고의 외형, 색상, 형태 등 디자인 관련 언급",
    "기타 - 위의 어떤 항목에도 명확히 해당되지 않는 기타 내용"
]

# ========================
# 3. 데이터 로딩
# ========================
with open("data/clean/cold.json", "r", encoding="utf-8") as f:
    topic_data = json.load(f)

sentences = [item["reply"] for item in topic_data]

# ========================
# 4. 분류 시작
# ========================
categorized_comments = {label: [] for label in raw_labels}
threshold = 0.6

for i, sentence in enumerate(sentences):
    result = classifier(sentence, labels, multi_label=False)
    label_with_desc = result["labels"][0]
    score = result["scores"][0]

    # 라벨 설명 제거
    best_label = label_with_desc.split(" - ")[0]

    if score < threshold:
        best_label = "기타"

    # 안전하게 추가
    if best_label not in categorized_comments:
        categorized_comments["기타"].append({
            "index": i,
            "text": sentence,
            "score": round(score, 4),
            "note": f"Missing label: {best_label}"
        })
    else:
        categorized_comments[best_label].append({
            "index": i,
            "text": sentence,
            "score": round(score, 4)
        })

# ========================
# 5. 저장
# ========================
output_path = "data/categorized_comments.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(categorized_comments, f, indent=2, ensure_ascii=False)

# ========================
# 6. 요약 출력
# ========================
for label in raw_labels:
    print(f"[{label}] → {len(categorized_comments[label])}개")

print(f"\n✅ 저장 완료: {output_path}")
