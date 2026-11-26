"""Базовый HTTP-клиент к стенду qa-internship.avito.com."""

import json
from typing import Any, Optional

import allure
import requests

BASE_URL = "https://qa-internship.avito.com"


class ApiClient:
    """Общая обёртка над requests: base URL, session, Bearer."""

    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def set_token(self, token: Optional[str]) -> None:
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
        else:
            self.session.headers.pop("Authorization", None)

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        url = f"{self.base_url}{path}"
        with allure.step(f"{method.upper()} {path}"):
            self._attach_request(method, url, json, headers)
            response = self.session.request(method, url, json=json, headers=headers, **kwargs)
            self._attach_response(response)
            return response

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    @staticmethod
    def _attach_request(
        method: str,
        url: str,
        body: Optional[dict[str, Any]],
        headers: Optional[dict[str, str]],
    ) -> None:
        payload = {
            "method": method.upper(),
            "url": url,
            "headers": headers or {},
            "body": body,
        }
        allure.attach(
            json.dumps(payload, ensure_ascii=False, indent=2),
            name="request",
            attachment_type=allure.attachment_type.JSON,
        )

    @staticmethod
    def _attach_response(response: requests.Response) -> None:
        allure.attach(
            str(response.status_code),
            name="status_code",
            attachment_type=allure.attachment_type.TEXT,
        )
        try:
            body: Any = response.json()
            text = json.dumps(body, ensure_ascii=False, indent=2)
            attachment_type = allure.attachment_type.JSON
        except ValueError:
            text = response.text
            attachment_type = allure.attachment_type.TEXT

        allure.attach(
            text,
            name="response_body",
            attachment_type=attachment_type,
        )
