from dataclasses import dataclass

from app.services.evaluation.score_calculator import (
    calculate_expected_points_score,
    calculate_keyword_score,
    calculate_quality_score,
    calculate_structure_score,
    clamp_score,
)
from app.services.evaluation.text_normalizer import word_count


@dataclass(slots=True)
class EvaluationResult:
    score: float
    feedback: str
    strengths: list[str]
    weaknesses: list[str]
    missed_points: list[str]
    source: str = "local"


def evaluate_locally(answer: str, keywords: list[str], expected_points: list[str]) -> EvaluationResult:
    point_score, covered_points, missed_points = calculate_expected_points_score(answer, expected_points)
    keyword_score = calculate_keyword_score(answer, keywords)
    quality_score = calculate_quality_score(answer)
    structure_score = calculate_structure_score(answer)
    score = clamp_score(point_score + keyword_score + quality_score + structure_score)

    strengths: list[str] = []
    weaknesses: list[str] = []
    if covered_points:
        strengths.append(f"Covered {len(covered_points)} expected point(s).")
    if keyword_score >= 15:
        strengths.append("Used important terminology.")
    if word_count(answer) >= 25:
        strengths.append("Answer has enough detail.")
    if missed_points:
        weaknesses.append("Some expected points are missing.")
    if word_count(answer) < 12:
        weaknesses.append("Answer is too short.")
    if not strengths:
        strengths.append("The answer gives a starting point for discussion.")

    feedback = (
        f"Score {score}/100. "
        f"Coverage: {round(point_score, 1)}/45, keywords: {round(keyword_score, 1)}/25, "
        f"explanation: {round(quality_score, 1)}/20, structure: {round(structure_score, 1)}/10."
    )
    return EvaluationResult(score, feedback, strengths, weaknesses, missed_points)

