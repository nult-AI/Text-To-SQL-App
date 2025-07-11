import os, json
from openai import OpenAI         

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

_SYSTEM_PROMPT = """
You convert natural-language questions into read-only SQLite SQL.
Never output INSERT / UPDATE / DELETE.
Return JSON: { "sql": "...", "thought": "..." }.
"""

def text_to_sql(question: str, schema: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",         
        temperature=0.1,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user",
             "content": f"schema:\n{schema}\n\nquestion: {question}"}
        ]
    )
    payload = json.loads(response.choices[0].message.content)
    return payload["sql"]
