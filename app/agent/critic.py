# from app.llm.client import call_llm

# def review(step: str, observation: str) -> bool:
#     prompt = f"""
# You are a critic agent.
# Step: {step}
# Observation: {observation}

# Is the observation relevant, correct, and useful?
# Reply with only ACCEPT or REJECT.
# """
#     result = call_llm(prompt)
#     return "ACCEPT" in result.upper()

import re, json
from app.llm.client import call_llm

def review(step, result, state):
    """
    Review tool output with explanation and confidence.
    Accepts string or dict results.
    """
    tool_name = step.split(":")[0].strip().lower()

    if tool_name == "analyze_code":
        return {
            "verdict": "ACCEPT",
            "reason": "Analysis should not be rejected",
            "improved_step": step,
            "confidence": 0.9
        }
    if isinstance(result, str):
        result_dict = {"stdout": result, "success": True}
    else:
        result_dict = result

    prompt = f"""
You are a senior AI code reviewer.
Return ONLY valid JSON.

Format:
{{
  "verdict": "ACCEPT" or "REJECT",
  "reason": "...",
  "improved_step": "...",
  "confidence": float (0-1)
}}

Step:
{step}

Current Code:
{state.current_code}

Result:
{result_dict.get('stdout', '')}

Test Execution:
Success: {result_dict.get('success', 'unknown')}
Errors: {result_dict.get('stderr', '')}

Language:
{state.language or "unknown"}

RULE:
- If Test Execution Success is false → MUST return REJECT
- If JSON cannot be parsed → MUST return REJECT
"""

    raw = call_llm(prompt)
    raw = re.sub(r"```[a-zA-Z]*\n", "", raw).replace("```", "").replace("\r", "").replace("\t", "\\t")

    try:
        return json.loads(raw)
    except Exception:
        return {
            "verdict": "REJECT",
            "reason": f"Invalid JSON from LLM: {raw}",
            "improved_step": step,
            "confidence": 0.0
        }