"""Автотесты статистики. TC-STAT-01, TC-STAT-02."""

from typing import Any

import allure
from api.items import ItemsApi
from api.statistics import StatisticsApi

from tests.helpers import extract_item_id

DEFAULT_STATS = {"likes": 7, "viewCount": 13, "contacts": 3}

pytestmark = [allure.epic("API"), allure.feature("Statistics")]


def test_tc_stat_01_statistic_v1(
    items_api: ItemsApi,
    statistics_api: StatisticsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-STAT-01 - Статистика объявления v1."""
    create_response = items_api.create(
        seller_id=authorized_user["id"],
        name="autotest stats v1",
        price=1000,
        statistics=DEFAULT_STATS,
    )
    assert create_response.status_code == 200
    item_id = extract_item_id(create_response)

    response = statistics_api.get_v1(item_id)

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 1
    stats = body[0]
    assert stats["likes"] == DEFAULT_STATS["likes"]
    assert stats["viewCount"] == DEFAULT_STATS["viewCount"]
    assert stats["contacts"] == DEFAULT_STATS["contacts"]

    items_api.delete(item_id)


def test_tc_stat_02_statistic_v2(
    items_api: ItemsApi,
    statistics_api: StatisticsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-STAT-02 - Статистика объявления v2."""
    create_response = items_api.create(
        seller_id=authorized_user["id"],
        name="autotest stats v2",
        price=1000,
        statistics=DEFAULT_STATS,
    )
    assert create_response.status_code == 200
    item_id = extract_item_id(create_response)

    response = statistics_api.get_v2(item_id)

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) >= 1
    stats = body[0]
    assert stats["likes"] == DEFAULT_STATS["likes"]
    assert stats["viewCount"] == DEFAULT_STATS["viewCount"]
    assert stats["contacts"] == DEFAULT_STATS["contacts"]

    items_api.delete(item_id)
