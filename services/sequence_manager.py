from __future__ import annotations

import json
import os
import threading
from pathlib import Path

_LOCK = threading.Lock()


def reserve_sequence(path: Path, count: int) -> int:
    """Reserve a continuous, persistent number range and return its first number.

    The counter is written atomically. Reserved numbers are never reused, even if a
    later batch operation fails; this is intentional to guarantee uniqueness.
    """
    if count < 1:
        raise ValueError("Kayıt sayısı en az 1 olmalıdır.")

    path.parent.mkdir(parents=True, exist_ok=True)
    with _LOCK:
        next_number = 1
        if path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                next_number = max(1, int(payload.get("next_form_number", 1)))
            except (OSError, ValueError, TypeError, json.JSONDecodeError):
                next_number = 1

        updated = {"next_form_number": next_number + count}
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(updated, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.replace(temporary, path)
        return next_number
