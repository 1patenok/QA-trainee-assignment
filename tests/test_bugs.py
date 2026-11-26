"""Негативы с известными дефектами стенда.

Ожидаем корректное поведение API. Если стенд врёт — тест падает
с сообщением и ссылкой на BUG-XXX в BUGS.md (как в ТЗ).
"""

from typing import Any

import allure
from api.auth import AuthApi
from api.items import ItemsApi

from tests.helpers import extract_item_id

DEFAULT_STATS = {"likes": 1, "viewCount": 1, "contacts": 1}
PASSWORD = "strong-password"

pytestmark = [allure.epic("API"), allure.feature("Known bugs")]


def test_tc_item_05_negative_price(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-ITEM-05 - цена -1 должна отклоняться. См. BUG-032."""
    response = items_api.create(
        seller_id=authorized_user["id"],
        name="bug negative price",
        price=-1,
        statistics=DEFAULT_STATS,
    )
    try:
        assert response.status_code >= 400, (
            f"BUG-032: ожидали 4xx для price=-1, получили {response.status_code}. См. BUGS.md"
        )
    finally:
        if response.status_code == 200:
            items_api.delete(extract_item_id(response))


def test_tc_item_06_zero_price_message(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-ITEM-06 - при price=0 текст не должен врать про 'обязательно'. См. BUG-033."""
    response = items_api.create(
        seller_id=authorized_user["id"],
        name="bug zero price",
        price=0,
        statistics=DEFAULT_STATS,
    )
    assert response.status_code == 400, (
        f"BUG-033: ожидали 400 для price=0, получили {response.status_code}. См. BUGS.md"
    )
    text = response.text.lower()
    assert "обязательно" not in text, (
        f"BUG-033: при price=0 не должно быть 'обязательно'. Ответ: {response.text}. См. BUGS.md"
    )


def test_tc_item_08_negative_likes(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-ITEM-08 - likes=-1 должен отклоняться. См. BUG-034."""
    response = items_api.create(
        seller_id=authorized_user["id"],
        name="bug negative likes",
        price=100,
        statistics={"likes": -1, "viewCount": 1, "contacts": 1},
    )
    try:
        assert response.status_code >= 400, (
            f"BUG-034: ожидали 4xx для likes=-1, получили {response.status_code}. См. BUGS.md"
        )
    finally:
        if response.status_code == 200:
            items_api.delete(extract_item_id(response))


def test_tc_item_09_negative_view_count(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-ITEM-09 - viewCount=-1 должен отклоняться. См. BUG-034."""
    response = items_api.create(
        seller_id=authorized_user["id"],
        name="bug negative views",
        price=100,
        statistics={"likes": 1, "viewCount": -1, "contacts": 1},
    )
    try:
        assert response.status_code >= 400, (
            f"BUG-034: ожидали 4xx для viewCount=-1, получили {response.status_code}. См. BUGS.md"
        )
    finally:
        if response.status_code == 200:
            items_api.delete(extract_item_id(response))


def test_tc_item_10_negative_contacts(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-ITEM-10 - contacts=-1 должен отклоняться. См. BUG-034."""
    response = items_api.create(
        seller_id=authorized_user["id"],
        name="bug negative contacts",
        price=100,
        statistics={"likes": 1, "viewCount": 1, "contacts": -1},
    )
    try:
        assert response.status_code >= 400, (
            f"BUG-034: ожидали 4xx для contacts=-1, получили {response.status_code}. См. BUGS.md"
        )
    finally:
        if response.status_code == 200:
            items_api.delete(extract_item_id(response))


def test_tc_item_15_price_as_string(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-ITEM-15 - отказ ок, сообщение не про 'тело объявления'. См. BUG-035."""
    response = items_api.create_raw(
        {
            "sellerID": authorized_user["id"],
            "name": "bug price string",
            "price": "100",
            "statistics": DEFAULT_STATS,
        }
    )
    assert response.status_code == 400, (
        f"BUG-035: ожидали 400 для price строкой, получили {response.status_code}. См. BUGS.md"
    )
    status = str(response.json().get("status", "")).lower()
    assert "тело объявления" not in status, (
        f"BUG-035: сообщение врёт про тело объявления: {status}. См. BUGS.md"
    )


def test_tc_del_03_double_delete(
    items_api: ItemsApi,
    authorized_user: dict[str, Any],
) -> None:
    """TC-DEL-03 - повторный DELETE: 404 без status 500 в теле. См. BUG-036."""
    create_response = items_api.create(
        seller_id=authorized_user["id"],
        name="bug double delete",
        price=100,
        statistics=DEFAULT_STATS,
    )
    assert create_response.status_code == 200
    item_id = extract_item_id(create_response)

    first = items_api.delete(item_id)
    assert first.status_code == 200

    second = items_api.delete(item_id)
    assert second.status_code == 404, (
        f"BUG-036: ожидали HTTP 404 при повторном DELETE, получили {second.status_code}. "
        "См. BUGS.md"
    )
    body = second.json()
    assert str(body.get("status")) != "500", (
        f"BUG-036: в теле status=500 при HTTP 404: {body}. См. BUGS.md"
    )
    message = body.get("result", {}).get("message")
    assert message, f"BUG-036: пустое message в теле: {body}. См. BUGS.md"


def test_tc_reg_03_empty_username(auth_api: AuthApi) -> None:
    """TC-REG-03 - пустой username, сообщение не про JSON. См. BUG-037."""
    response = auth_api.register("", PASSWORD)
    assert response.status_code == 400, (
        f"BUG-037: ожидали 400, получили {response.status_code}. См. BUGS.md"
    )
    assert response.json().get("error") != "invalid JSON body", (
        f"BUG-037: при валидном JSON нельзя отвечать 'invalid JSON body': {response.text}. "
        "См. BUGS.md"
    )


def test_tc_reg_04_empty_password(auth_api: AuthApi) -> None:
    """TC-REG-04 - пустой password, сообщение не про JSON. См. BUG-037."""
    response = auth_api.register("student_empty_pwd_check", "")
    assert response.status_code == 400, (
        f"BUG-037: ожидали 400, получили {response.status_code}. См. BUGS.md"
    )
    assert response.json().get("error") != "invalid JSON body", (
        f"BUG-037: при валидном JSON нельзя отвечать 'invalid JSON body': {response.text}. "
        "См. BUGS.md"
    )


def test_tc_auth_03_empty_password(
    auth_api: AuthApi,
    registered_user: dict[str, Any],
) -> None:
    """TC-AUTH-03 - пустой password при autorize, сообщение не про JSON. См. BUG-037."""
    response = auth_api.autorize(registered_user["username"], "")
    assert response.status_code in (400, 401), (
        f"BUG-037: ожидали 400/401, получили {response.status_code}. См. BUGS.md"
    )
    assert response.json().get("error") != "invalid JSON body", (
        f"BUG-037: при валидном JSON нельзя отвечать 'invalid JSON body': {response.text}. "
        "См. BUGS.md"
    )
