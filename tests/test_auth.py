"""Автотесты авторизации. TC-AUTH-01, TC-AUTH-02, TC-AUTH-04."""

import time
from typing import Any

import allure
from api.auth import AuthApi

pytestmark = [allure.epic("API"), allure.feature("Authorize")]


def test_tc_auth_01_successful_autorize(
    auth_api: AuthApi,
    registered_user: dict[str, Any],
) -> None:
    """TC-AUTH-01 - Успешная авторизация."""
    response = auth_api.autorize(
        registered_user["username"],
        registered_user["password"],
    )

    assert response.status_code == 200
    body = response.json()
    assert "accessToken" in body
    assert body.get("tokenType") == "Bearer"


def test_tc_auth_02_wrong_password(
    auth_api: AuthApi,
    registered_user: dict[str, Any],
) -> None:
    """TC-AUTH-02 - Неверный пароль."""
    response = auth_api.autorize(
        registered_user["username"],
        "wrong-password",
    )

    assert response.status_code == 401
    body = response.json()
    assert body.get("error") == "invalid username or password"
    assert "accessToken" not in body


def test_tc_auth_04_nonexistent_user(auth_api: AuthApi) -> None:
    """TC-AUTH-04 - Авторизация несуществующего пользователя."""
    username = f"no_such_user_{int(time.time() * 1000)}"
    response = auth_api.autorize(username, "strong-password")

    assert response.status_code == 401
    body = response.json()
    assert body.get("error") == "invalid username or password"
    assert "accessToken" not in body
