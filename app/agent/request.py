from pydantic import BaseModel

class AgentRequest(BaseModel):
    goal: str
    code: str
    language: str = "python"
