"""Проверки доступа. TC-ACCESS-01 … TC-ACCESS-09."""

from typing import Any

import allure
import pytest
from api.client import ApiClient
from api.items import ItemsApi

from tests.helpers import extract_item_id

DEFAULT_STATS = {"likes": 1, "viewCount": 1, "contacts": 1}
FAKE_ITEM_ID = "00000000-0000-0000-0000-000000000001"
AUTH_ERROR = "valid bearer token is required"

pytestmark = [allure.epic("API"), allure.feature("Access")]


def test_tc_access_01_create_without_token(api: ApiClient) -> None:
    """TC-ACCESS-01 - создание без токена."""
    response = api.post(
        "/api/1/item",
        json={
            "sellerID": 1,
            "name": "no token",
            "price": 100,
            "statistics": DEFAULT_STATS,
        },
    )
    assert response.status_code == 401
    assert response.json().get("error") == AUTH_ERROR


def test_tc_access_02_create_with_invalid_token(api: ApiClient) -> None:
    """TC-ACCESS-02 - создание с невалидным токеном."""
    api.set_token("not-a-real-token")
    response = api.post(
        "/api/1/item",
        json={
            "sellerID": 1,
            "name": "bad token",
            "price": 100,
            "statistics": DEFAULT_STATS,
        },
    )
    assert response.status_code == 401
    assert response.json().get("error") == AUTH_ERROR


def test_tc_access_03_foreign_seller_id(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-ACCESS-03 - чужой sellerID."""
    response = items_api.create(
        seller_id=1,
        name="alien seller",
        price=100,
        statistics=DEFAULT_STATS,
    )
    assert response.status_code == 400
    assert "sellerID должен совпадать" in response.text


@pytest.mark.parametrize(
    "method,path",
    [
        ("GET", f"/api/1/item/{FAKE_ITEM_ID}"),
        ("GET", "/api/1/1/item"),
        ("GET", f"/api/1/statistic/{FAKE_ITEM_ID}"),
        ("GET", f"/api/2/statistic/{FAKE_ITEM_ID}"),
        ("DELETE", f"/api/2/item/{FAKE_ITEM_ID}"),
    ],
    ids=[
        "TC-ACCESS-04",
        "TC-ACCESS-05",
        "TC-ACCESS-06",
        "TC-ACCESS-07",
        "TC-ACCESS-08",
    ],
)
def test_tc_access_protected_without_token(
    api: ApiClient,
    method: str,
    path: str,
) -> None:
    """TC-ACCESS-04…08 - защищённые ручки без токена."""
    response = api.request(method, path)
    assert response.status_code == 401
    assert response.json().get("error") == AUTH_ERROR


def test_tc_access_09_x_userid_does_not_impersonate(
    api: ApiClient,
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-ACCESS-09 - X-UserId не подменяет владельца."""
    response = api.post(
        "/api/1/item",
        json={
            "sellerID": authorized_user["id"],
            "name": "x-userid check",
            "price": 100,
            "statistics": DEFAULT_STATS,
        },
        headers={"X-UserId": "1"},
    )
    assert response.status_code == 200
    item_id = extract_item_id(response)

    get_response = items_api.get_by_id(item_id)
    assert get_response.status_code == 200
    item = get_response.json()[0]
    assert item["sellerId"] == authorized_user["id"]

    items_api.delete(item_id)
