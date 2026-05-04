import logging

from app.llm.client import call_llm

def detect_language(code: str) -> str:
    code_lower = code.lower()
    if "def " in code_lower or "import " in code_lower:
        return "python"
    elif "function " in code_lower or "console.log" in code_lower or "parseint" in code_lower:
        return "javascript"
    elif "public class" in code_lower or "@test" in code_lower:
        return "java"
    return "unknown"


def fix_code(code: str, analysis: dict = None, language: str = "python") -> dict:
    prompt = f"""
You are an expert software engineer.

Fix the following {language} code.

Issues detected:
{analysis}

Requirements:
- Fix syntax and logical bugs
- Keep code valid and runnable
- Keep the function signature unchanged
- DO NOT translate into another language.
- KEEP the code in {language.upper()} only.
-RETURN ONLY VALID {language.upper()} CODE.
-NO explanation, NO markdown, NO ```.

Important:
- Ensure code is executable in a test environment
- If code uses input/IO, replace it with function parameters
- If no function exists, wrap logic into a function
- Return values instead of printing when possible

Code:
{code}

Return only the fixed code.
"""
    try:
        fixed_code = call_llm(prompt).strip()
        fixed_code = "\n".join(line.rstrip() for line in fixed_code.splitlines() if line.strip())
        if not fixed_code:
            raise ValueError("Empty response from LLM")
        # detected = detect_language(fixed_code)
        # if detected != language:
        #     logging.warning(f"Language mismatch: expected {language}, got {detected}")
        #     return {
        #         "success": False,
        #         "stdout": "",
        #         "stderr": f"LLM drifted to {detected} instead of {language}"
        #     }
        return {"success": True, "stdout": fixed_code, "stderr": ""}
    except Exception as e:
        logging.error(f"fix_code failed: {e}")
        return {"success": False, "stdout": "", "stderr": str(e)}

fix_code.needs_code = True
fix_code.accepts_language = True