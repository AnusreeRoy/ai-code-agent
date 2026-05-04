import time, logging
from app.agent.state import AgentState
from app.agent.critic import review
from app.tools.registry import TOOL_MAP, select_tool
from app.agent.validator import validate_step_output
from app.tools.web import web_search

MAX_RETRIES = 3
STEP_DELAY = 0.5

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')


def execute(state: AgentState) -> AgentState:
    if "run_tests" in state.plan and "generate_tests" not in state.plan:
        idx = state.plan.index("run_tests")
        state.plan.insert(idx, "generate_tests")
        logging.info("Inserted generate_tests before run_tests")
        
    VALID_STEPS = set(TOOL_MAP.keys())

    if any(step not in VALID_STEPS for step in state.plan):
        raise ValueError(f"Corrupted plan detected: {state.plan}")
    
    while state.current_step < len(state.plan):
        step = state.plan[state.current_step]
        tool = select_tool(step)

        fail_reasons = []
        logging.info(f"Executing step {state.current_step + 1}/{len(state.plan)}: {step} ({tool.__name__})")

        for attempt in range(1, MAX_RETRIES + 1):

            # Prepare input for tool
            if tool.__name__ == "run_tests":
                if not state.tests or not state.tests.strip():
                   logging.warning("No tests found → generating tests")

                   test_tool = select_tool("generate_tests")
                   test_output = test_tool(state.current_code, state.language)
           
                   if test_output.get("success"):
                       state.tests = test_output["stdout"]
                   else:
                       fail_reasons.append("test_generation_failed")
                       time.sleep(STEP_DELAY)
                       continue
                output = tool(state.current_code, state.tests, state.language)

                # Force fail if tests failed
                if not output.get("success", False):
                    reason = output.get("stderr", "tests_failed")
                    fail_reasons.append(reason)
                    logging.warning(f"Tests failed ❌: {reason}")
                    logging.info("Retrying by fixing code...")
                    
                    analyze_tool = select_tool("analyze_code")
                    analysis_output = analyze_tool(state.current_code, state.language)
                    
                    if analysis_output.get("success"):
                        state.analysis = analysis_output["stdout"]

                    fix_tool = select_tool("fix_code")
                    fix_output = fix_tool(state.current_code, state.analysis, state.language)
                
                    if fix_output.get("success"):
                        state.current_code = fix_output["stdout"]
                    else:
                        fail_reasons.append("fix_after_test_failed")
                    if "test_failure" in reason:
                        search_query = f"fix {reason} in {state.language} code"
                        search_results = web_search(search_query)
                        fail_reasons.append(f"Web search results: {search_results}")
                    time.sleep(STEP_DELAY)
                    continue  # retry automatically

            elif getattr(tool, "needs_code", False):
                args = [state.current_code]
                
                if tool.__name__ == "fix_code" and state.analysis:
                    args.append(state.analysis)

                if getattr(tool, "accepts_language", False) and state.language:
                    args.append(state.language)

                output = tool(*args)

            else:
                output = tool(step)

            # Normalize output
            if isinstance(output, str):
                output = {"success": True, "stdout": output, "stderr": ""}

            print(f"\n➡️ STEP: {step}")
            print(f"🛠 TOOL: {tool.__name__}")
            print(f"📤 OUTPUT: {output}")

            # Handle failed tool execution
            if not output.get("success", False):
                reason = output.get("stderr", "Unknown")
                fail_reasons.append(reason)
                logging.warning(f"Attempt {attempt}/{MAX_RETRIES} failed: {reason}")
                step = f"{step} | Last issue: {reason}"
                time.sleep(STEP_DELAY)
                continue

            if tool.__name__ == "run_tests":
                result = output  # keep full structure
            else:
                result = output["stdout"]

            # Validate output first
            if not validate_step_output(tool.__name__, result):
                reason = "validation_failed"
                fail_reasons.append(reason)
                logging.warning(f"Validation failed ❌ — {reason}")
                step = f"{step} | Last issue: {reason}"
                time.sleep(STEP_DELAY)
                continue

            # Critic review
            critique = review(step, result, state)
            if critique["verdict"] == "ACCEPT":
                # Save results based on tool type
                if tool.__name__ in ["fix_code", "optimize_code"]:
                    state.current_code = result
                elif tool.__name__ == "generate_tests":
                    state.tests = result
                elif tool.__name__ == "analyze_code":
                    state.analysis = result
                elif tool.__name__ == "run_tests":
                    state.test_results = result

                # Log step observation
                state.observations.append({
                    "step": step,
                    "tool": tool.__name__,
                    "result": result,
                    "fail_reasons": fail_reasons.copy()
                })

                state.current_step += 1
                break  # move to next plan step

            else:
                reason = critique.get("reason", "critic_rejected")
                fail_reasons.append(reason)
                step = critique.get("improved_step", step)
                step = f"{step} | Last issue: {reason}"
                logging.warning(f"Critic REJECTED ❌: {reason}")
                logging.info(f"Retrying with improved step: {step}")
                time.sleep(STEP_DELAY)

        else:
            # Permanently failed step: after all retries, move on
            logging.error(f"Step permanently failed after {MAX_RETRIES} attempts: {step}")
            state.observations.append({
                "step": step,
                "tool": tool.__name__,
                "result": None,
                "fail_reasons": fail_reasons.copy()
            })
            state.current_step += 1  # Move on to the next step in the plan

        time.sleep(STEP_DELAY)

    return state