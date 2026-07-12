from pydantic import BaseModel, Field


class AnswerCreate(BaseModel):
    question_id: int
    answer_text: str = Field(min_length=1, max_length=10000)


class AnswerOut(BaseModel):
    score: float
    feedback: str
    strengths: list[str]
    weaknesses: list[str]
    missed_points: list[str]
    evaluation_source: str

