from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.utils.json_helpers import write_json

QUESTION_DIR = Path("data/questions")
LEVELS = ["intern", "junior", "middle", "senior"]

QUESTION_BANK = {
    "python": {
        "categories": ["python_core", "oop", "fastapi", "sql", "testing", "async_python", "docker", "algorithms"],
        "prompts": [
            ("Чем list отличается от tuple?", "mutable immutable list tuple", ["list is mutable", "tuple is immutable", "syntax and use cases differ"]),
            ("Что такое генератор и когда он полезен?", "generator yield lazy memory", ["generators are lazy", "yield returns values one by one", "useful for streams"]),
            ("Как работает GIL и где он мешает?", "gil threads cpu io", ["GIL protects interpreter state", "CPU-bound threads are limited", "I/O-bound tasks still benefit"]),
            ("Зачем нужны context managers?", "with enter exit resource", ["manage resources", "guarantee cleanup", "implement __enter__ and __exit__"]),
            ("Как FastAPI валидирует входные данные?", "fastapi pydantic validation schema", ["Pydantic validates data", "type hints drive schema", "invalid data returns 422"]),
            ("Что делает async/await в Python?", "async await event loop coroutine", ["coroutines cooperate", "event loop schedules work", "best for I/O"]),
            ("Как написать хороший unit test?", "pytest arrange act assert fixture", ["isolated behavior", "clear assertions", "fixtures reduce setup"]),
            ("Что такое SQL-инъекция и как её предотвратить?", "sql injection parameters orm", ["avoid string concatenation", "use parameters", "validate inputs"]),
            ("Как устроена MRO в Python?", "mro inheritance c3 super", ["method resolution order", "C3 linearization", "super follows MRO"]),
            ("Когда стоит использовать dataclass?", "dataclass boilerplate repr init", ["reduces boilerplate", "good for data containers", "supports type hints"]),
        ],
    },
    "java": {
        "categories": ["java_core", "oop", "spring", "sql", "concurrency"],
        "prompts": [
            ("Что такое JVM?", "jvm bytecode runtime gc", ["runs bytecode", "provides runtime", "manages memory"]),
            ("Чем interface отличается от abstract class?", "interface abstract inheritance contract", ["interfaces define contract", "abstract classes can share state", "multiple interfaces allowed"]),
            ("Как работает garbage collection?", "garbage collection heap reachability", ["tracks reachable objects", "frees heap memory", "different collectors exist"]),
            ("Что такое dependency injection?", "dependency injection spring bean", ["dependencies are provided", "improves testability", "Spring manages beans"]),
            ("Как избежать race condition?", "race condition synchronization locks", ["shared state causes races", "use synchronization", "prefer immutable data"]),
        ],
    },
    "javascript": {
        "categories": ["javascript_core", "async_js", "dom", "rest_api", "testing"],
        "prompts": [
            ("Что такое event loop?", "event loop microtask macrotask async", ["single-threaded loop", "tasks queues", "promises use microtasks"]),
            ("Чем let отличается от var?", "let var scope hoisting", ["block scope", "var function scope", "temporal dead zone"]),
            ("Как работает Promise?", "promise async then catch", ["represents future value", "states pending fulfilled rejected", "supports chaining"]),
            ("Что такое closure?", "closure lexical scope function", ["function captures scope", "keeps variables alive", "useful for encapsulation"]),
            ("Как обработать ошибку fetch?", "fetch error status catch", ["check response status", "catch network errors", "handle JSON parsing"]),
        ],
    },
    "backend": {
        "categories": ["rest_api", "databases", "architecture", "security", "caching"],
        "prompts": [
            ("Что делает API RESTful?", "rest resource http stateless", ["resource-oriented URLs", "HTTP methods", "stateless requests"]),
            ("Когда нужен кэш?", "cache latency load invalidation", ["reduces latency", "lowers database load", "requires invalidation strategy"]),
            ("Что такое идемпотентность?", "idempotent retry put delete", ["same request same effect", "important for retries", "PUT and DELETE usually idempotent"]),
            ("Как проектировать пагинацию?", "pagination limit offset cursor", ["limit response size", "offset or cursor", "stable ordering matters"]),
            ("Что такое rate limiting?", "rate limiting abuse quota", ["limits requests", "protects service", "can be per user or IP"]),
        ],
    },
    "frontend": {
        "categories": ["html", "css", "accessibility", "performance", "browser_apis"],
        "prompts": [
            ("Что такое semantic HTML?", "semantic html accessibility structure", ["meaningful tags", "helps accessibility", "improves SEO"]),
            ("Как работает CSS specificity?", "css specificity cascade selector", ["selectors have weights", "cascade resolves conflicts", "inline is strongest"]),
            ("Как улучшить доступность формы?", "accessibility label focus aria", ["use labels", "visible focus", "ARIA only when needed"]),
            ("Что такое critical rendering path?", "rendering css js layout paint", ["browser parses HTML/CSS", "layout and paint", "blocking resources matter"]),
            ("Как оптимизировать изображения?", "image compression responsive lazy", ["compress images", "responsive sizes", "lazy loading"]),
        ],
    },
    "qa": {
        "categories": ["testing_theory", "test_cases", "automation", "api_testing", "bugs"],
        "prompts": [
            ("Чем smoke test отличается от regression test?", "smoke regression scope", ["smoke checks basics", "regression checks old features", "different scope"]),
            ("Как написать хороший баг-репорт?", "bug report steps expected actual", ["clear steps", "expected vs actual", "environment and evidence"]),
            ("Что тестировать в API?", "api status schema auth edge", ["status codes", "response schema", "auth and edge cases"]),
            ("Что такое test pyramid?", "test pyramid unit integration e2e", ["many unit tests", "fewer integration tests", "few E2E tests"]),
            ("Как выбирать cases for automation?", "automation stable repeatable value", ["repeatable cases", "stable flows", "high business value"]),
        ],
    },
    "devops": {
        "categories": ["linux", "docker", "ci_cd", "networking", "monitoring"],
        "prompts": [
            ("Что такое Docker image?", "docker image layer container", ["image is template", "layers are cached", "container runs image"]),
            ("Что должно быть в CI pipeline?", "ci test lint build deploy", ["install dependencies", "lint and test", "build artifact"]),
            ("Как читать логи сервиса?", "logs timestamp level trace", ["check timestamps", "levels matter", "correlate with traces"]),
            ("Что такое healthcheck?", "healthcheck readiness liveness", ["checks service health", "used by orchestrators", "can separate readiness"]),
            ("Как диагностировать сетевую проблему?", "network dns ping curl port", ["check DNS", "check connectivity", "check ports and firewall"]),
        ],
    },
    "data_analyst": {
        "categories": ["sql", "statistics", "python", "visualization", "metrics"],
        "prompts": [
            ("Чем INNER JOIN отличается от LEFT JOIN?", "inner left join null", ["inner keeps matches", "left keeps left rows", "missing right values are NULL"]),
            ("Что такое медиана?", "median distribution outliers", ["middle value", "robust to outliers", "requires sorted data"]),
            ("Как выбрать метрику продукта?", "metric goal behavior guardrail", ["linked to goal", "captures behavior", "guardrail metrics prevent harm"]),
            ("Когда использовать histogram?", "histogram distribution bins", ["shows distribution", "uses bins", "good for numeric data"]),
            ("Как проверить качество данных?", "data quality missing duplicates consistency", ["missing values", "duplicates", "consistency checks"]),
        ],
    },
    "hr": {
        "categories": ["motivation", "teamwork", "conflict", "leadership", "communication"],
        "prompts": [
            ("Расскажите о сложном конфликте в команде.", "conflict team communication resolution", ["describe context", "explain actions", "show outcome"]),
            ("Почему вам интересна эта роль?", "motivation role company growth", ["connect skills", "company interest", "growth path"]),
            ("Как вы реагируете на критику?", "feedback criticism improve", ["listen carefully", "clarify examples", "turn feedback into action"]),
            ("Расскажите о сильной стороне.", "strength example impact", ["name strength", "give example", "show impact"]),
            ("Как вы планируете обучение?", "learning plan priorities practice", ["set priorities", "practice regularly", "measure progress"]),
        ],
    },
    "general": {
        "categories": ["algorithms", "git", "databases", "system_design", "communication"],
        "prompts": [
            ("Что такое Big O?", "big o complexity time space", ["describes growth", "time or space complexity", "worst case often used"]),
            ("Как работает Git merge?", "git merge branch conflict", ["combines histories", "may create merge commit", "conflicts need resolution"]),
            ("Зачем нужны индексы в базе данных?", "index database query performance", ["speed up reads", "cost writes and storage", "choose by query patterns"]),
            ("Что такое горизонтальное масштабирование?", "scaling horizontal instances load", ["add instances", "use load balancing", "state must be shared or externalized"]),
            ("Как объяснить сложную идею новичку?", "communication simplify analogy feedback", ["simplify terms", "use examples", "check understanding"]),
        ],
    },
}


def translations(ru: str) -> dict[str, str]:
    return {
        "ru": ru,
        "en": f"Explain: {ru}",
        "uk": f"Поясніть: {ru}",
    }


def build_questions(profession: str, config: dict) -> list[dict]:
    result: list[dict] = []
    prompts = config["prompts"]
    categories = config["categories"]
    counter = 1
    for level in LEVELS:
        for index in range(5):
            prompt, keyword_text, expected = prompts[index % len(prompts)]
            category = categories[index % len(categories)]
            result.append(
                {
                    "id": f"{profession}_{level}_{counter:03d}",
                    "profession": profession,
                    "level": level,
                    "category": category,
                    "question": translations(prompt),
                    "keywords": keyword_text.split(),
                    "expected_points": expected,
                    "difficulty": LEVELS.index(level) + 1,
                    "max_score": 100,
                }
            )
            counter += 1
    return result


def main() -> None:
    for profession, config in QUESTION_BANK.items():
        write_json(QUESTION_DIR / f"{profession}.json", build_questions(profession, config))
    total = sum(len(build_questions(name, config)) for name, config in QUESTION_BANK.items())
    print(f"Seeded {total} questions into {QUESTION_DIR}")


if __name__ == "__main__":
    main()
