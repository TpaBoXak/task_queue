from pydantic import BaseModel
from pydantic import Field
from typing import Optional
from datetime import datetime

class TaskBaseSchema(BaseModel):
    title: Optional[str] = Field(default="Без названия", max_length=50)

class TaskSchema(BaseModel):
    title: str
    status: str
    create_time: Optional[datetime]
    start_time: Optional[datetime]
    time_to_execute: Optional[int] = Field(ge=0, le=10)


class TaskCompletionRequest(BaseModel):
    task_id: int
    time_start: datetime
    time_to_exec: int = Field(ge=0, le=10)