import openai
from app.config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

def summarize_with_gpt(comments: list) -> str:
    prompt = "다음은 유튜브 댓글 목록입니다:\n" + "\n".join(comments) + "\n\n요약해줘."

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 유튜브 댓글을 요약하는 AI입니다."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature=0.7
    )

    return response.choices[0].message.content
