from difflib import SequenceMatcher

from app.services.evaluation.text_normalizer import normalize_text, word_count


def clamp_score(score: float) -> float:
    return round(max(0, min(100, score)), 2)


def calculate_keyword_score(answer: str, keywords: list[str]) -> float:
    normalized_answer = normalize_text(answer)
    if not keywords:
        return 0.0
    found = sum(1 for keyword in keywords if normalize_text(keyword) in normalized_answer)
    return found / len(keywords) * 25


def calculate_expected_points_score(answer: str, expected_points: list[str]) -> tuple[float, list[str], list[str]]:
    normalized_answer = normalize_text(answer)
    covered: list[str] = []
    missed: list[str] = []
    for point in expected_points:
        normalized_point = normalize_text(point)
        words = [word for word in normalized_point.split() if len(word) > 3]
        direct_hit = normalized_point in normalized_answer
        fuzzy_hit = SequenceMatcher(None, normalized_answer, normalized_point).ratio() > 0.42
        word_hit = bool(words) and sum(word in normalized_answer for word in words) >= max(1, len(words) // 2)
        if direct_hit or fuzzy_hit or word_hit:
            covered.append(point)
        else:
            missed.append(point)
    if not expected_points:
        return 20.0, covered, missed
    return len(covered) / len(expected_points) * 45, covered, missed


def calculate_quality_score(answer: str) -> float:
    words = word_count(answer)
    if words < 8:
        return 2
    if words < 25:
        return 10
    if words < 80:
        return 17
    return 20


def calculate_structure_score(answer: str) -> float:
    normalized = normalize_text(answer)
    connectors = ["because", "for example", "first", "second", "поэтому", "например", "во-первых", "также"]
    score = 4 if word_count(answer) >= 12 else 1
    if any(connector in normalized for connector in connectors):
        score += 3
    if any(marker in answer for marker in [".", ";", ":", "\n", "-"]):
        score += 3
    return min(10, score)

