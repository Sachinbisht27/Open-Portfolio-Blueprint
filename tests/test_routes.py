from __future__ import annotations

import pytest

from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/projects",
        "/projects/dost",
        "/contact",
        "/resume",
    ],
)
def test_routes_render_successfully(client, path: str) -> None:
    response = client.get(f"{path}?lang=en")
    assert response.status_code == 200


def test_language_cookie_is_set(client) -> None:
    response = client.get("/?lang=ta")
    cookie_header = response.headers.get("Set-Cookie", "")

    assert "portfolio_lang=ta" in cookie_header


def test_arabic_sets_rtl_document_direction(client) -> None:
    response = client.get("/?lang=ar")
    html = response.data.decode("utf-8")

    assert 'lang="ar"' in html
    assert 'dir="rtl"' in html


def test_language_switcher_is_present(client) -> None:
    response = client.get("/projects?lang=en")
    html = response.data.decode("utf-8")

    assert 'id="languageSwitcher"' in html
