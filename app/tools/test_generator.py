from app.llm.client import call_llm

import logging
from app.llm.client import call_llm
from app.tools.bug_fixer import detect_language
def generate_tests(code: str, language: str = "python") -> dict:
    prompt = f"""
Generate {language.upper()} unit tests for the existing function only.
Strict rules:
- DO NOT redefine the function itself.
- Return only valid {language.upper()} code for tests.
- Cover normal, edge, and error cases.
- Use the correct test framework (`@Test` for Java, `assert` for Python, console.assert or if(...) throw Error for JS).
- Wrap multiple assertions in a single function or code block to avoid incomplete files.
- DO NOT translate into another language.
- KEEP the code in {language.upper()} only.
- NO explanations, NO markdown, NO ```.
Code:
{code}
"""
    try:
        tests_code = call_llm(prompt).strip()
        if not tests_code:
            # fallback scaffold
            tests_code = f"# No tests generated for {language.upper()}"
            
        # detected = detect_language(tests_code)
        # if detected != language:
        #     logging.warning(f"Language mismatch: expected {language}, got {detected}")
            # return {
            #     "success": False,
            #     "stdout": "",
            #     "stderr": f"LLM drifted to {detected} instead of {language}"
            # }
        return {"success": True, "stdout": tests_code, "stderr": ""}
    except Exception as e:
        logging.error(f"generate_tests failed: {e}")
        # fallback error scaffold
        return {
            "success": False,
            "stdout": f"# Test generation failed for {language.upper()}",
            "stderr": str(e),
        }

generate_tests.needs_code = True
generate_tests.accepts_language = True
