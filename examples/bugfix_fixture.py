"""Small fixed fixture used to prove bugfix workflows require a regression check."""

ALLOWED_STATUSES = frozenset({"active", "inactive"})


def is_allowed_status(value: str) -> bool:
    return value in ALLOWED_STATUSES
