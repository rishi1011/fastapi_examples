from pydantic import BaseModel
from typing import Optional

class Task(BaseModel):
    title: str
    description: str
    status: str

class TaskWithID(Task):
    id: int
    
class TaskV2(BaseModel):
    title: str
    description: str
    status: str
    priority: str | None = "lower"

class TaskV2WithID(TaskV2):
    id: int
