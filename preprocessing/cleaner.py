import json
import re
import html

# 텍스트 정제 함수
def clean_text(text):
    text = html.unescape(text)
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)  # 이모지 제거
    text = re.sub(r'[ㅋㅎㅠㅜ]{2,}', ' ', text)
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'[^가-힣a-zA-Z0-9\s.,!?]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 경로 설정
input_path = "/Users/jiyu/projects/sothat/sothat-nlp/data/response.json"
output_path = "/Users/jiyu/projects/sothat/sothat-nlp/data/cleaned_response.json"

# 파일 불러오기
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# reply 필드 정제
for item in data:
    item['reply'] = clean_text(item['reply'])

# 정제된 결과 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)