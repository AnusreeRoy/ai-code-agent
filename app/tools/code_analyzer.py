import logging
from app.llm.client import call_llm

def analyze_code(code: str, language: str = "python") -> dict:
    prompt = f"""
Analyze this {language.upper()} code.
- Identify bugs, inefficiencies, and improvement opportunities.
- Return structured JSON with fields: issues[], suggestions[].
- NO extra text, NO markdown.

Code:
{code}
"""
    try:
        raw = call_llm(prompt).strip()
        if not raw:
            raise ValueError("Empty response from LLM")

        import json
        analysis = json.loads(raw)
        return {"success": True, "stdout": analysis, "stderr": ""}
    except Exception as e:
        logging.error(f"analyze_code failed: {e}")
        return {"success": False, "stdout": {}, "stderr": str(e)}

analyze_code.needs_code = True
analyze_code.accepts_language = True