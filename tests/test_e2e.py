"""Сквозной сценарий. TC-E2E-01."""

import time

import allure
from api.auth import AuthApi
from api.items import ItemsApi
from api.statistics import StatisticsApi

from tests.helpers import extract_item_id

PASSWORD = "strong-password"
DEFAULT_STATS = {"likes": 5, "viewCount": 10, "contacts": 2}

pytestmark = [allure.epic("API"), allure.feature("E2E")]


@allure.story("TC-E2E-01")
@allure.title("Register → autorize → create → get → stats → delete")
def test_tc_e2e_01_full_item_flow(
    auth_api: AuthApi,
    items_api: ItemsApi,
    statistics_api: StatisticsApi,
    api,
) -> None:
    """TC-E2E-01 - register → autorize → create → get → stats → delete → get 404."""
    username = f"student_e2e_{int(time.time() * 1000)}"

    with allure.step("Регистрация пользователя"):
        register_response = auth_api.register(username, PASSWORD)
        assert register_response.status_code == 201
        seller_id = register_response.json()["id"]

    with allure.step("Авторизация и установка Bearer"):
        auth_response = auth_api.autorize(username, PASSWORD)
        assert auth_response.status_code == 200
        token = auth_response.json()["accessToken"]
        api.set_token(token)

    with allure.step("Создание объявления"):
        create_response = items_api.create(
            seller_id=seller_id,
            name="e2e item",
            price=999,
            statistics=DEFAULT_STATS,
        )
        assert create_response.status_code == 200
        item_id = extract_item_id(create_response)

    with allure.step("Получение объявления по id"):
        get_response = items_api.get_by_id(item_id)
        assert get_response.status_code == 200
        assert get_response.json()[0]["id"] == item_id

    with allure.step("Статистика v1 и v2"):
        stat_v1 = statistics_api.get_v1(item_id)
        assert stat_v1.status_code == 200
        assert stat_v1.json()[0]["likes"] == DEFAULT_STATS["likes"]

        stat_v2 = statistics_api.get_v2(item_id)
        assert stat_v2.status_code == 200
        assert stat_v2.json()[0]["likes"] == DEFAULT_STATS["likes"]

    with allure.step("Удаление и проверка 404"):
        delete_response = items_api.delete(item_id)
        assert delete_response.status_code == 200

        after_delete = items_api.get_by_id(item_id)
        assert after_delete.status_code == 404
