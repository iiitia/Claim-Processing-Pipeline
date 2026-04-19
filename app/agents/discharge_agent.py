import json
from app.llm import generate


def discharge_agent(pages):
    text = "\n".join(p["text"] if isinstance(p, dict) else p for p in pages)

    if not text.strip():
        return {}

    prompt = f"""
Extract in JSON:

{{
  "diagnosis": "",
  "admission_date": "",
  "discharge_date": "",
  "doctor_name": ""
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
        print("❌ discharge_agent error:", e)
        return {"raw": res} if res else {}