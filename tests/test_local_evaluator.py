from app.services.evaluation.local_evaluator import evaluate_locally


def test_local_evaluator_scores_good_answer():
    result = evaluate_locally(
        "A list is mutable while a tuple is immutable. Lists are useful when data changes, tuples for fixed data.",
        ["mutable", "immutable", "list", "tuple"],
        ["list is mutable", "tuple is immutable", "syntax and use cases differ"],
    )
    assert result.score >= 60
    assert result.missed_points


def test_local_evaluator_flags_short_answer():
    result = evaluate_locally("I do not know", ["mutable"], ["list is mutable"])
    assert result.score < 60
    assert "Answer is too short." in result.weaknesses

