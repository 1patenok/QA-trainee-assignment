"""Лёгкие нефункциональные проверки. TC-NF-01, TC-NF-02."""

from typing import Any

import allure
from api.client import ApiClient
from api.items import ItemsApi

from tests.helpers import extract_item_id

DEFAULT_STATS = {"likes": 1, "viewCount": 1, "contacts": 1}
MAX_SECONDS = 5.0
FAKE_ITEM_ID = "00000000-0000-0000-0000-000000000001"

pytestmark = [allure.epic("API"), allure.feature("Non-functional")]


def test_tc_nf_01_create_response_time(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-NF-01 - create укладывается в разумное время."""
    response = items_api.create(
        seller_id=authorized_user["id"],
        name="nf timing",
        price=100,
        statistics=DEFAULT_STATS,
    )
    assert response.status_code == 200
    assert response.elapsed.total_seconds() <= MAX_SECONDS
    items_api.delete(extract_item_id(response))


def test_tc_nf_02_unauthorized_response_time(api: ApiClient) -> None:
    """TC-NF-02 - 401 без токена приходит быстро."""
    response = api.get(f"/api/1/item/{FAKE_ITEM_ID}")
    assert response.status_code == 401
    assert response.elapsed.total_seconds() <= MAX_SECONDS
