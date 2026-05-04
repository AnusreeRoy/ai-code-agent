from fastapi import FastAPI
from app.agent.request import AgentRequest
from app.agent.state import AgentState
from app.agent.planner import create_plan
from app.agent.executor import execute
from app.agent.writer import write_output
# from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev (restrict later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def clean_code(code: str):
    return code.strip().replace("\\n", "\n")

@app.post("/run_agent")
def run_agent(req: AgentRequest):
    try:
        state = AgentState(
            goal=req.goal,
            code=clean_code(req.code),
            language=req.language
        )

        state.plan = create_plan(req.goal, state.language)
        state = execute(state)
        final_output = write_output(state)

        return {
            "goal": state.goal or "",
            "language": state.language or "",
            "plan": state.plan or [],
            "final_code": state.current_code or "# No code generated",
            "tests": state.tests or "# No tests generated",
            "analysis": state.analysis or {"issues": [], "suggestions": []},
            "result": final_output or {}
        }

    except Exception as e:
        return {
            "error": str(e),
            "goal": req.goal,
            "language": req.language,
            "plan": [],
            "final_code": "# Error occurred",
            "tests": "# Error occurred",
            "analysis": {"issues": [], "suggestions": []},
            "result": {}
        }
