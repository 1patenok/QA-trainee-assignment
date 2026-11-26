"""Ручки статистики объявления."""

import requests

from api.client import ApiClient


class StatisticsApi:
    """GET /api/1/statistic/{id} и GET /api/2/statistic/{id}."""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def get_v1(self, item_id: str) -> requests.Response:
        return self._client.get(f"/api/1/statistic/{item_id}")

    def get_v2(self, item_id: str) -> requests.Response:
        return self._client.get(f"/api/2/statistic/{item_id}")
