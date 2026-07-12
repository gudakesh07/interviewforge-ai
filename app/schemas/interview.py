from pydantic import BaseModel, Field


class InterviewCreate(BaseModel):
    profession: str = Field(min_length=2, max_length=60)
    level: str = Field(min_length=2, max_length=30)
    interview_type: str = Field(min_length=2, max_length=40)
    language: str = Field(default="ru", max_length=8)
    selected_technologies: list[str] = Field(default_factory=list, max_length=12)
    requested_question_count: int = Field(default=5, ge=1, le=20)


class InterviewOut(BaseModel):
    id: int
    profession: str
    level: str
    interview_type: str
    language: str
    status: str
    total_score: float

    model_config = {"from_attributes": True}

