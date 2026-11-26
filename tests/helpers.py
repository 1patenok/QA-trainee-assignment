"""Вспомогательные функции для тестов."""

import re

import requests

UUID_RE = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",
    re.IGNORECASE,
)


def extract_item_id(response: requests.Response) -> str:
    """Достаёт uuid объявления из ответа create (поле status или весь JSON)."""
    body = response.json()
    text = str(body.get("status", "")) + " " + str(body)
    match = UUID_RE.search(text)
    assert match is not None, f"uuid не найден в ответе: {body}"
    return match.group(0)
