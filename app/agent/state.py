# from pydantic import BaseModel
# from typing import List, Optional

# class AgentState(BaseModel):
#     goal: str
#     plan: List[str] = []
#     current_step: int = 0
#     observations: List[str] = []
#     retries: int = 0
#     final_output: Optional[str] = None
class AgentState:
    def __init__(self, goal: str, code: str, language: str = "python"):
        self.goal = goal
        self.original_code = code
        self.current_code = code

        self.language = language
        self.tests_language = language   

        self.plan = []
        self.current_step = 0
        self.observations = []

        self.tests = ""
        self.analysis = ""