import os, json
from google import genai         

client = genai.Client()

_SYSTEM_PROMPT = """
You convert natural-language questions into read-only SQLite SQL.
Never output INSERT / UPDATE / DELETE.
Return JSON: { "sql": "...", "thought": "..." }.
"""

def text_to_sql(question: str, schema: str) -> str:
    # 1. Tạo nội dung cho lời nhắc (prompt)
    full_prompt = f"{_SYSTEM_PROMPT}\n\nschema:\n{schema}\n\nquestion: {question}"
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",         
        contents=[
            full_prompt
        ],
        config=genai.types.GenerateContentConfig(
            # Kích hoạt JSON Mode để Gemini chỉ trả về một đối tượng JSON hợp lệ
            response_mime_type="application/json",
            temperature=0.1
        )
    )
    # 3. Phân tích cú pháp JSON và trích xuất SQL
    # Đầu ra JSON của Gemini được trả về trong response.text khi dùng JSON mode
    try:
        payload = json.loads(response.text)
        return payload["sql"]
    except json.JSONDecodeError:
        print(f"Lỗi phân tích JSON: {response.text}")
        return ""
    except KeyError:
        print(f"Lỗi: Không tìm thấy khóa 'sql' trong {response.text}")
        return ""
