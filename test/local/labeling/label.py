import streamlit as st
import os
import json

# === 경로 설정 ==
INPUT_FILE = "/Users/jiyu/projects/sothat/sothat-nlp/data/clean/cleaned_2_raw2.json"
OUTPUT_FILE = "/Users/jiyu/projects/sothat/sothat-nlp/data/label/labeled_2_raw2.json"

# === 라벨 정의 ===
BINARY_LABELS = {0: "무의미", 1: "유의미"}
CATEGORY_OPTIONS = ["perform", "design", "price", "compare"]

# === 데이터 로딩 ===
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# 이전 라벨링 불러오기 (있으면)
labeled_data = []
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        labeled_data = json.load(f)

labeled_indices = {item["index"] for item in labeled_data}
current_index = len(labeled_data)

# === 라벨링 UI ===
st.title("📝 리뷰 라벨링 툴 (성능, 디자인, 가격, 비교)")
st.markdown("**1단계:** 댓글이 의미 있는지 판단 → 의미 있다면 2단계 다중 라벨 선택")

if current_index >= len(raw_data):
    st.success("✅ 모든 리뷰 라벨링 완료!")
    st.stop()

item = raw_data[current_index]
text = item["text"] if isinstance(item, dict) and "text" in item else item

# 리뷰 표시
st.markdown(f"**리뷰 {current_index+1}/{len(raw_data)}:**")
with st.expander("📝 리뷰 펼쳐보기", expanded=True):
    st.markdown(f"""
    <div style='white-space: pre-wrap; background-color:#f9f9f9; padding:10px; border-radius:10px; font-size:16px;'>
        {text}
    </div>
    """, unsafe_allow_html=True)

# 1단계 라벨 선택
binary_label = st.radio("이 댓글이 의미 있는가?", list(BINARY_LABELS.values()), horizontal=True)

# 2단계 멀티라벨 선택
selected_categories = []
if binary_label == "유의미":
    selected_categories = st.multiselect("해당되는 모든 카테고리를 선택하세요:", CATEGORY_OPTIONS)

# 저장 버튼
if st.button("✅ 라벨 저장"):
    entry = {
        "index": current_index,
        "text": text,
        "binary_label": 1 if binary_label == "유의미" else 0,
        "category_labels": selected_categories if binary_label == "유의미" else []
    }

    labeled_data.append(entry)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(labeled_data, f, ensure_ascii=False, indent=2)

    st.rerun()
