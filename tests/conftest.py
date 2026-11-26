"""Общие фикстуры: клиент, API-слои, пользователь с токеном."""

import time
from typing import Any

import allure
import pytest
from api.auth import AuthApi
from api.client import BASE_URL, ApiClient
from api.items import ItemsApi
from api.statistics import StatisticsApi

DEFAULT_PASSWORD = "strong-password"


@pytest.fixture(autouse=True)
def _allure_environment() -> None:
    """Пишет окружение в Allure (base URL стенда)."""
    allure.dynamic.parameter("base_url", BASE_URL)


@pytest.fixture
def api() -> ApiClient:
    return ApiClient()


@pytest.fixture
def auth_api(api: ApiClient) -> AuthApi:
    return AuthApi(api)


@pytest.fixture
def items_api(api: ApiClient) -> ItemsApi:
    return ItemsApi(api)


@pytest.fixture
def statistics_api(api: ApiClient) -> StatisticsApi:
    return StatisticsApi(api)


@pytest.fixture
def registered_user(auth_api: AuthApi) -> dict[str, Any]:
    """Новый пользователь на каждый тест (уникальный username)."""
    username = f"student_{int(time.time() * 1000)}"
    response = auth_api.register(username, DEFAULT_PASSWORD)
    body = response.json()
    return {
        "id": body["id"],
        "username": body["username"],
        "password": DEFAULT_PASSWORD,
        "response": response,
    }


@pytest.fixture
def authorized_user(
    api: ApiClient,
    auth_api: AuthApi,
    registered_user: dict[str, Any],
) -> dict[str, Any]:
    """Зарегистрированный пользователь + Bearer на api-сессии."""
    response = auth_api.autorize(
        registered_user["username"],
        registered_user["password"],
    )
    token = response.json()["accessToken"]
    api.set_token(token)
    return {
        **registered_user,
        "access_token": token,
        "auth_response": response,
    }
