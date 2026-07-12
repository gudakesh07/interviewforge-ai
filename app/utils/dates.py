from datetime import datetime


def utcnow() -> datetime:
    return datetime.utcnow()


def seconds_between(start: datetime, end: datetime | None = None) -> int:
    finish = end or utcnow()
    return max(0, int((finish - start).total_seconds()))

