import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.services.question_service import load_questions


def main() -> None:
    print(f"Available questions: {len(load_questions())}")


if __name__ == "__main__":
    main()
