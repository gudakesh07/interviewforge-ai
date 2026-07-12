import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.utils.json_helpers import read_json

REQUIRED_KEYS = {"id", "profession", "level", "category", "question", "keywords", "expected_points", "difficulty", "max_score"}


def main() -> None:
    total = 0
    for path in Path("data/questions").glob("*.json"):
        questions = read_json(path)
        if not isinstance(questions, list):
            raise SystemExit(f"{path} must contain a list")
        for question in questions:
            missing = REQUIRED_KEYS - set(question)
            if missing:
                raise SystemExit(f"{path}: missing keys {missing}")
            for language in ("ru", "en", "uk"):
                if language not in question["question"]:
                    raise SystemExit(f"{path}: missing language {language}")
        total += len(questions)
    if total < 200:
        raise SystemExit(f"Expected at least 200 questions, got {total}")
    print(f"Validated {total} questions")


if __name__ == "__main__":
    main()
