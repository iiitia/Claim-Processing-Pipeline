import json
from app.llm import generate


def id_agent(pages):
    text = "\n".join(p["text"] if isinstance(p, dict) else p for p in pages)

    if not text.strip():
        return {}

    prompt = f"""
Extract in JSON:

{{
  "full_name": "",
  "date_of_birth": "",
  "id_number": ""
}}

Return ONLY JSON. No explanation.

Text:
{text}
"""

    res = None
    try:
        res = generate(prompt).strip().replace("```json", "").replace("```", "")
        return json.loads(res)
    except Exception as e:
        print("❌ id_agent error:", e)
        return {"raw": res} if res else {}