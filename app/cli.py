import argparse
import asyncio

from app.services.evaluation.local_evaluator import evaluate_locally
from app.services.question_service import select_questions


async def practice(profession: str, level: str, count: int) -> None:
    questions = select_questions(profession, level, [], count, "quick")
    scores: list[float] = []
    for index, question in enumerate(questions, start=1):
        print(f"\nQuestion {index}: {question.question['en']}")
        answer = input("Your answer: ")
        result = evaluate_locally(answer, question.keywords, question.expected_points)
        scores.append(result.score)
        print(result.feedback)
    average = round(sum(scores) / len(scores), 2) if scores else 0
    print(f"\nFinal score: {average}/100")


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m app.cli")
    subparsers = parser.add_subparsers(dest="command", required=True)
    practice_parser = subparsers.add_parser("practice")
    practice_parser.add_argument("--profession", default="python")
    practice_parser.add_argument("--level", default="junior")
    practice_parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()
    if args.command == "practice":
        asyncio.run(practice(args.profession, args.level, args.count))


if __name__ == "__main__":
    main()

