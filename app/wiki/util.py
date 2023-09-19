def truncate_words(s: str, n: int = 5) -> str:
    return " ".join(s.split()[:n]) + "…"
