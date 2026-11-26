"""Автотесты объявлений. TC-ITEM-01 … TC-ITEM-04."""

from typing import Any

import allure
from api.items import ItemsApi

from tests.helpers import extract_item_id

DEFAULT_STATS = {"likes": 1, "viewCount": 2, "contacts": 3}
MISSING_ITEM_ID = "00000000-0000-0000-0000-000000000000"

pytestmark = [allure.epic("API"), allure.feature("Items")]


def test_tc_item_01_create_item(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-ITEM-01 - Успешное создание объявления."""
    response = items_api.create(
        seller_id=authorized_user["id"],
        name="autotest item",
        price=1500,
        statistics=DEFAULT_STATS,
    )

    assert response.status_code == 200
    item_id = extract_item_id(response)
    assert item_id

    items_api.delete(item_id)


def test_tc_item_02_get_item_by_id(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-ITEM-02 - Получение объявления по id."""
    name = "autotest get item"
    price = 2500
    create_response = items_api.create(
        seller_id=authorized_user["id"],
        name=name,
        price=price,
        statistics=DEFAULT_STATS,
    )
    assert create_response.status_code == 200
    item_id = extract_item_id(create_response)

    response = items_api.get_by_id(item_id)

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    item = body[0]
    assert item["id"] == item_id
    assert item["name"] == name
    assert item["price"] == price
    assert item["sellerId"] == authorized_user["id"]
    assert item["statistics"]["likes"] == DEFAULT_STATS["likes"]
    assert item["statistics"]["viewCount"] == DEFAULT_STATS["viewCount"]
    assert item["statistics"]["contacts"] == DEFAULT_STATS["contacts"]
    assert "createdAt" in item

    items_api.delete(item_id)


def test_tc_item_03_get_items_by_seller(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-ITEM-03 - Получение объявлений продавца."""
    create_response = items_api.create(
        seller_id=authorized_user["id"],
        name="autotest seller list",
        price=3000,
        statistics=DEFAULT_STATS,
    )
    assert create_response.status_code == 200
    item_id = extract_item_id(create_response)

    response = items_api.get_by_seller(authorized_user["id"])

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    ids = [item["id"] for item in body]
    assert item_id in ids

    items_api.delete(item_id)


def test_tc_item_04_get_nonexistent_item(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-ITEM-04 - Получение несуществующего объявления."""
    response = items_api.get_by_id(MISSING_ITEM_ID)

    assert response.status_code == 404
    body = response.json()
    message = str(body.get("result", {}).get("message", "")) + str(body)
    assert "not found" in message.lower()
