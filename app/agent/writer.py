from app.llm.client import call_llm
from app.agent.state import AgentState

# def write_output(state: AgentState) -> None:
#     prompt = f"""
# You are a senior industry analyst.

# Goal:
# {state.goal}

# You are given raw research notes below.
# Use ONLY this information.
# Do NOT invent facts.

# Research notes:
# {state.observations}

# Produce:
# - A short executive summary
# - A ranked list of top Tesla competitors
# - 1–2 lines of positioning per competitor

# If information is insufficient, say so explicitly.
# """

#     state.final_output = call_llm(prompt)

def write_output(state):
    explanation = call_llm(f"""
Goal: {state.goal}

Final Code ({state.language}):
{state.current_code}

Tests ({state.tests_language or 'unknown'}):
{state.tests}

Explain:
- what was fixed
- improvements made
- usage instructions
- respect language of each snippet
""")
    return {
        "language": state.language,
        "final_code": state.current_code,
        "tests": state.tests,
        "test_results": getattr(state, "test_results", {}),
        "observations": state.observations,
        "metrics": {
            "steps": len(state.observations),
            "failures": sum(len(o["fail_reasons"]) for o in state.observations)
        },
        "explanation": explanation,
    }