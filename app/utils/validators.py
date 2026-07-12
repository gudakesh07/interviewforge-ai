import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def clean_text(value: str, max_length: int = 10000) -> str:
    cleaned = value.replace("\x00", "").strip()
    return cleaned[:max_length]


def is_valid_email(value: str) -> bool:
    return bool(EMAIL_RE.match(value.strip()))

