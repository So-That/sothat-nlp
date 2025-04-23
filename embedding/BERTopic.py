import json
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
from collections import defaultdict

# 1. 댓글 로딩
with open("data/clean/cleand_headphone.json", "r", encoding="utf-8") as f:
    data = json.load(f)
texts = [item["reply"] for item in data]

# 2. 임베딩 모델
embedding_model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")

# 3. UMAP & CountVectorizer 세팅 (더 쪼개지게!)
umap_model = UMAP(n_neighbors=5, n_components=5, min_dist=0.0, metric='cosine')
vectorizer_model = CountVectorizer(ngram_range=(1, 2), stop_words="english")

# 4. BERTopic 생성
topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    vectorizer_model=vectorizer_model,
    language="multilingual",
    calculate_probabilities=True,
    min_topic_size=5,  # 작은 토픽도 살려서 더 많이 뽑기
    verbose=True
)

# 5. 학습
topics, probs = topic_model.fit_transform(texts)

# 6. 클러스터별로 묶기
clustered = defaultdict(list)
for topic_id, text in zip(topics, texts):
    clustered[f"topic_{topic_id}"].append(text)

# 7. 저장: 클러스터 → JSON
with open("bertopic_topic.json", "w", encoding="utf-8") as f:
    json.dump(clustered, f, ensure_ascii=False, indent=2)

# 8. 저장: 토픽 정보 (키워드 등) → CSV
topic_model.get_topic_info().to_csv("bertopic_topic.csv", index=False)

print("✅ 토픽 많이 쪼개서 저장 완료! → 'bertopic_topic.json', 'bertopic_topic.csv'")
