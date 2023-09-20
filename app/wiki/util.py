def truncate_words(s: str, n: int = 5) -> str:
    if len(s.split()) > n:
        return " ".join(s.split()[:n]) + "…"
    else:
        return s
