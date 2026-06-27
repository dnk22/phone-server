def normalize_identifier(value: str) -> str:
    normalized = value.strip().lower()
    if not normalized:
        raise ValueError("Identifier cannot be empty")
    return normalized
