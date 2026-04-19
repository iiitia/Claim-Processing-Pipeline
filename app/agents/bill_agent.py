import json
from app.llm import generate


def bill_agent(pages):
    text = "\n".join(p["text"] if isinstance(p, dict) else p for p in pages)

    if not text.strip():
        return {}

    prompt = f"""
Extract bill items in JSON format ONLY:

{{
  "items": [
    {{
      "item": "",
      "quantity": "",
      "rate": "",
      "amount": ""
    }}
  ],
  "total_amount": ""
}}

Return ONLY valid JSON. No explanation.

Text:
{text}
"""

    response = None
    try:
        response = generate(prompt)
        response = response.strip().replace("```json", "").replace("```", "")
        data = json.loads(response)
        return data

    except Exception as e:
        print("❌ bill_agent error:", e)
        return {"raw": response} if response else {}