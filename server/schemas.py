from pydantic import BaseModel, Field
from typing import List, Optional

class PatientData(BaseModel):
    user_name: str
    age: int = Field(gt=0, le=120)
    sex: str = Field(pattern="^(Male|Female|Other)$")
    symptoms: List[str]
    dietary_preferences: Optional[List[str]] = None

class ReportStatus(BaseModel):
    task_id: str
    status: str