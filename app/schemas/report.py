from pydantic import BaseModel


class ReportOut(BaseModel):
    overall_score: float
    technical_score: float
    communication_score: float
    strong_categories: list[str]
    weak_categories: list[str]
    recommendations: list[str]
    study_plan: list[dict]
    summary: str

    model_config = {"from_attributes": True}

