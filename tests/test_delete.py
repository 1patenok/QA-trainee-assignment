"""Автотесты удаления. TC-DEL-01, TC-DEL-02."""

from typing import Any

import allure
from api.items import ItemsApi

from tests.helpers import extract_item_id

DEFAULT_STATS = {"likes": 1, "viewCount": 1, "contacts": 1}

pytestmark = [allure.epic("API"), allure.feature("Delete")]


def test_tc_del_01_delete_item(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-DEL-01 - Успешное удаление объявления."""
    create_response = items_api.create(
        seller_id=authorized_user["id"],
        name="autotest delete",
        price=500,
        statistics=DEFAULT_STATS,
    )
    assert create_response.status_code == 200
    item_id = extract_item_id(create_response)

    response = items_api.delete(item_id)

    assert response.status_code == 200


def test_tc_del_02_get_after_delete(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-DEL-02 - GET после удаления объявления."""
    create_response = items_api.create(
        seller_id=authorized_user["id"],
        name="autotest get after delete",
        price=500,
        statistics=DEFAULT_STATS,
    )
    assert create_response.status_code == 200
    item_id = extract_item_id(create_response)

    delete_response = items_api.delete(item_id)
    assert delete_response.status_code == 200

    response = items_api.get_by_id(item_id)

    assert response.status_code == 404
    body = response.json()
    message = str(body.get("result", {}).get("message", "")) + str(body)
    assert "not found" in message.lower()
