import re
import unicodedata


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).lower()
    value = re.sub(r"[^\w\s+#.-]+", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def word_count(value: str) -> int:
    return len(normalize_text(value).split())

