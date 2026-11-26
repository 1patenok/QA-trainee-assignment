"""Ручки регистрации и авторизации."""

from typing import Any

import requests

from api.client import ApiClient


class AuthApi:
    """POST /api/1/register и POST /api/1/autorize."""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def register(self, username: str, password: str) -> requests.Response:
        body: dict[str, Any] = {"username": username, "password": password}
        return self._client.post("/api/1/register", json=body)

    def autorize(self, username: str, password: str) -> requests.Response:
        body: dict[str, Any] = {"username": username, "password": password}
        return self._client.post("/api/1/autorize", json=body)
