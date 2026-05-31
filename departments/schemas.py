from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class DepartmentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1, max_length=100)
    employee_ids: list[int] | None = None

class DepartmentUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1, max_length=100)
    employee_ids: list[int] | None = None

class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    employee_ids: list[int] = []

class DepartmentResponseId(DepartmentResponse):
    created_at: datetime
    updated_at: datetime | None = None