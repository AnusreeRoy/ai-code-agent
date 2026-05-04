# from app.tools.python import run_python
# from app.tools.web import web_search

# TOOLS = {
#     "python": run_python,
#     "web": web_search,
# }

# def select_tool(step: str):
#     if "search" in step.lower() or "web" in step.lower():
#         return TOOLS["web"]
#     return TOOLS["python"]

import logging
logging.basicConfig(level=logging.INFO)

from app.llm.client import call_llm
from app.tools import (
    bug_fixer,
    code_analyzer,
    code_optimizer,
    test_generator,
    web,
    python,
    runtime
)

TOOL_MAP = {
    "analyze_code": code_analyzer.analyze_code,
    "fix_code": bug_fixer.fix_code,
    "optimize_code": code_optimizer.optimize_code,
    "generate_tests": test_generator.generate_tests,
    "web_search": web.web_search,
    "run_python": python.run_python,
    "run_tests": runtime.run_tests
}

def select_tool(step: str):
    """
    STRICT TOOL ROUTER (NO FUZZY MATCHING)
    """

    if step not in TOOL_MAP:
        raise ValueError(f"Invalid tool step: {step}")

    return TOOL_MAP[step]