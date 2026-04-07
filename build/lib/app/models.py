from pydantic import BaseModel
from typing import Optional


# What agent sees
class Observation(BaseModel):
    diff: str
    task_type: str


# What agent sends
class Action(BaseModel):
    issue_type: str          # syntax | logic | performance
    description: str         # explanation of issue
    fix: str                 # suggested fix


# What env returns after step
class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Optional[dict] = None


# Internal task structure
class Task(BaseModel):
    id: str
    diff: str
    issue_type: str
    description_keywords: list[str]
    fix_keywords: list[str]
    difficulty: str  # easy | medium | hard