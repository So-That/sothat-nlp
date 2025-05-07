import os
import json
import re
import MeCab
import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans
# from sklearn.decomposition import PCA
# from sentence_transformers import SentenceTransformer

# 비속어 불러오기
with open('data/badwords.txt', 'r', encoding='utf-8-sig') as f:
    stopwords = set(f.read().split(","))

# 형태소 분석기 초기화
mecab = MeCab()

# 텍스트 전처리 함수
def clean_and_tokenize(text):
    text = re.sub(r"<.*?>", " ", text)  # HTML 태그 제거
    text = re.sub(r"[^\w\s가-힣]", " ", text)  # 특수문자 제거
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(ㅋ|ㅎ|ㅜ|ㅠ|ㄷ|ㅌ|ㄱ|ㅂ|ㅇ|ㄴ|ㅅ|ㅈ|ㅊ){1,}", " ", text)
    tokens = mecab.morphs(text)
    tokens = [t for t in tokens if t not in stopwords]
    return " ".join(tokens)

# 입력 파일 경로
input_path = "data/test/건조기.json"

# JSON 파일 로드
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 댓글 추출
sentences = [item["reply"] for item in data if "reply" in item and isinstance(item["reply"], str)]

# 댓글 전처리
processed_data = [{"reply": clean_and_tokenize(s)} for s in sentences]

# 저장 경로 생성 (data/clean/건조기.json 형태)
filename = os.path.basename(input_path)  # 건조기.json
output_dir = "data/clean"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, filename)

# 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(processed_data, f, ensure_ascii=False, indent=2)

print(f"✅ 전처리된 데이터를 {output_path}에 저장했습니다.")
