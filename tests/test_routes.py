from __future__ import annotations

from copy import deepcopy
import re

import pytest

from app import app
from app import views


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
        "/projects/case-study",
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


def test_mobile_rtl_timeline_alignment_rule_exists(client) -> None:
    response = client.get("/static/style.css")
    stylesheet = response.data.decode("utf-8")

    assert response.status_code == 200
    assert '[dir="rtl"] .timeline::before' in stylesheet
    assert "right: 20px;" in stylesheet
    assert "transform: translateX(50%);" in stylesheet


def test_asset_version_query_param_is_stable(client) -> None:
    first_response = client.get("/?lang=en")
    second_response = client.get("/?lang=en")

    first_html = first_response.data.decode("utf-8")
    second_html = second_response.data.decode("utf-8")

    style_pattern = r'style\.css\?v=([^"]+)'
    first_version_match = re.search(style_pattern, first_html)
    second_version_match = re.search(style_pattern, second_html)

    assert first_version_match is not None
    assert second_version_match is not None
    assert first_version_match.group(1) == second_version_match.group(1)


def test_contact_quick_links_resolve_by_social_label(client, monkeypatch) -> None:
    localized_site = deepcopy(views.get_localized_site_config("en"))
    localized_site["social_links"] = list(reversed(localized_site["social_links"]))
    localized_site["contact"].pop("quick_links", None)

    monkeypatch.setattr(views, "get_localized_site_config", lambda _: localized_site)

    response = client.get("/contact?lang=en")
    html = response.data.decode("utf-8")

    linkedin_url = next(
        link["url"]
        for link in localized_site["social_links"]
        if link["label"] == "LinkedIn"
    )
    github_url = next(
        link["url"]
        for link in localized_site["social_links"]
        if link["label"] == "GitHub"
    )

    linkedin_quick_link = (
        f'href="{linkedin_url}" target="_blank" rel="noopener noreferrer" '
        'class="btn ghost full-width-btn"'
    )
    github_quick_link = (
        f'href="{github_url}" target="_blank" rel="noopener noreferrer" '
        'class="btn ghost full-width-btn"'
    )

    assert linkedin_quick_link in html
    assert github_quick_link in html
