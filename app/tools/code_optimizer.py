from app.llm.client import call_llm

import logging
from app.llm.client import call_llm

def optimize_code(code: str, language: str = "python") -> dict:
    prompt = f"""
Optimize and refactor this {language.upper()} code for:
- Performance
- Readability
- Maintainability

RETURN ONLY VALID {language.upper()} CODE.
NO explanation.
NO markdown.
NO ```.

Code:
{code}
"""
    try:
        optimized_code = call_llm(prompt).strip()
        if not optimized_code:
            raise ValueError("Empty response from LLM")
        return {"success": True, "stdout": optimized_code, "stderr": ""}
    except Exception as e:
        logging.error(f"optimize_code failed: {e}")
        return {"success": False, "stdout": "", "stderr": str(e)}

optimize_code.needs_code = True
optimize_code.accepts_language = True