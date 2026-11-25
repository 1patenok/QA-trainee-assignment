"""Ручки объявлений."""

from typing import Any
import requests
from api.client import ApiClient


class ItemsApi:
    """POST/GET/DELETE объявлений."""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def create(
        self,
        seller_id: int,
        name: str,
        price: int,
        statistics: dict[str, Any],
        **extra: Any,
    ) -> requests.Response:
        body: dict[str, Any] = {
            "sellerID": seller_id,
            "name": name,
            "price": price,
            "statistics": statistics,
        }
        body.update(extra)
        return self._client.post("/api/1/item", json=body)

    def create_raw(self, body: dict[str, Any]) -> requests.Response:
        """Создание с произвольным телом (для негативных кейсов)."""
        return self._client.post("/api/1/item", json=body)

    def get_by_id(self, item_id: str) -> requests.Response:
        return self._client.get(f"/api/1/item/{item_id}")

    def get_by_seller(self, seller_id: int) -> requests.Response:
        return self._client.get(f"/api/1/{seller_id}/item")

    def delete(self, item_id: str) -> requests.Response:
        return self._client.delete(f"/api/2/item/{item_id}")
