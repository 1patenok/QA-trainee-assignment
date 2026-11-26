"""Негативы валидации объявления (стенд отвечает корректно). TC-ITEM-07, 11–14."""

from typing import Any

import allure
import pytest
from api.items import ItemsApi

DEFAULT_STATS = {"likes": 1, "viewCount": 1, "contacts": 1}

pytestmark = [allure.epic("API"), allure.feature("Items validation")]


def test_tc_item_07_empty_name(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-ITEM-07 - пустой name."""
    response = items_api.create(
        seller_id=authorized_user["id"],
        name="",
        price=100,
        statistics=DEFAULT_STATS,
    )
    assert response.status_code == 400
    assert "поле name обязательно" in response.text


@pytest.mark.parametrize(
    "missing_field,expected_fragment",
    [
        ("name", "поле name обязательно"),
        ("price", "поле price обязательно"),
        ("statistics", "поле likes обязательно"),
        ("sellerID", "поле sellerID обязательно"),
    ],
    ids=["TC-ITEM-11", "TC-ITEM-12", "TC-ITEM-13", "TC-ITEM-14"],
)
def test_tc_item_missing_required_field(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
    missing_field: str,
    expected_fragment: str,
) -> None:
    """TC-ITEM-11…14 - отсутствие обязательного поля."""
    body: dict[str, Any] = {
        "sellerID": authorized_user["id"],
        "name": "missing field check",
        "price": 100,
        "statistics": DEFAULT_STATS,
    }
    del body[missing_field]

    response = items_api.create_raw(body)

    assert response.status_code == 400
    assert expected_fragment in response.text
