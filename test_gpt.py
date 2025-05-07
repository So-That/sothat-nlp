from app.gpt import summarize_with_gpt

if __name__ == "__main__":
    comments = [
        "이 제품 정말 좋아요. 특히 배터리가 오래 가요.",
        "디자인은 예쁜데 조금 무거운 편이에요.",
        "가성비는 괜찮지만 발열이 심해요."
    ]

    result = summarize_with_gpt(comments)
    print("\n🧠 GPT 요약 결과:\n")
    print(result)
