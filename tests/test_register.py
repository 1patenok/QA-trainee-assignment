"""Автотесты регистрации. TC-REG-01, TC-REG-02."""

import time
from typing import Any

import allure
from api.auth import AuthApi

PASSWORD = "strong-password"

pytestmark = [allure.epic("API"), allure.feature("Register")]


def test_tc_reg_01_successful_register(auth_api: AuthApi) -> None:
    """TC-REG-01 - Успешная регистрация."""
    username = f"student_{int(time.time() * 1000)}"

    response = auth_api.register(username, PASSWORD)

    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["username"] == username


def test_tc_reg_02_duplicate_username(
    auth_api: AuthApi,
    registered_user: dict[str, Any],
) -> None:
    """TC-REG-02 - Повторная регистрация того же username."""
    response = auth_api.register(
        registered_user["username"],
        registered_user["password"],
    )

    assert response.status_code != 201
    body = response.json()
    assert body.get("error") == "username is already registered"
