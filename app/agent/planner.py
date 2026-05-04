from app.llm.client import call_llm

import json
import logging
from app.llm.client import call_llm

VALID_STEPS = {
    "analyze_code",
    "fix_code",
    "generate_tests",
    "optimize_code",
    "run_tests"
}

def create_plan(goal: str, language: str) -> list[str]:
    prompt = f"""
You are an AI planning agent.

Goal: {goal}
Language: {language}

Available tools:
- analyze_code
- fix_code
- generate_tests
- optimize_code
- run_tests

Return ONLY valid JSON:

{{
  "steps": ["analyze_code", "fix_code", "generate_tests", "optimize_code", "run_tests"]
}}

Rules:
- Steps MUST be chosen ONLY from available tools
- NO explanations
- NO extra keys
"""

    raw = call_llm(prompt)

    print("\n🧠 RAW PLAN OUTPUT:\n", raw)

    try:
        data = json.loads(raw)
        steps = data.get("steps", [])

        # HARD VALIDATION
        clean_steps = []
        for s in steps:
            if s in VALID_STEPS:
                clean_steps.append(s)
            else:
                raise ValueError(f"Invalid step in plan: {s}")

        return clean_steps

    except Exception as e:
        logging.error(f"Plan parsing failed: {e}")
        return []