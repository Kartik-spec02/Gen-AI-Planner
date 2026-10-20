from pydantic import BaseModel, Field
from typing import Optional
from llm_service import generate_plan
from database import save_plan

class Brief(BaseModel):
    event_type: str = Field(..., description="wedding|birthday|community")
    theme: str = "elegant"
    budget: float = Field(..., gt=0)
    guests: int = Field(..., gt=0, le=100000)
    date: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = ""

def create_plan(brief: Brief) -> dict:
    plan = generate_plan(brief.model_dump())
    plan["id"] = save_plan(brief.model_dump(), plan)
    return plan
