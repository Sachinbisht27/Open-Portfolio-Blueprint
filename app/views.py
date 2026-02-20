from __future__ import annotations

from datetime import datetime
import hashlib
import os
from pathlib import Path
import re

import flask
from flask import g, request

from app import app
from app.content import (
    RTL_LANGUAGES,
    SUPPORTED_LANGUAGES,
    get_localized_site_config,
    normalize_language,
    translate,
)

STATIC_ASSET_FILES = ("style.css", "script.js")


def _build_asset_version() -> str:
    configured_version = os.getenv("ASSET_VERSION")
    if configured_version:
        return configured_version

    static_directory = Path(app.static_folder or "app/static")
    version_digest = hashlib.sha256()

    for filename in STATIC_ASSET_FILES:
        asset_path = static_directory / filename
        if not asset_path.exists():
            continue

        file_stats = asset_path.stat()
        version_digest.update(filename.encode("utf-8"))
        version_digest.update(str(file_stats.st_mtime_ns).encode("utf-8"))
        version_digest.update(str(file_stats.st_size).encode("utf-8"))

    return version_digest.hexdigest()[:12] or "dev"


ASSET_VERSION = _build_asset_version()


def _social_key(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


@app.before_request
def set_language_context() -> None:
    requested_language = request.args.get("lang")
    cookie_language = request.cookies.get("portfolio_lang")
    language_code = normalize_language(requested_language or cookie_language)

    g.current_language = language_code
    g.is_rtl = language_code in RTL_LANGUAGES


@app.context_processor
def inject_template_context() -> dict[str, object]:
    current_language = getattr(g, "current_language", "en")
    site = get_localized_site_config(current_language)
    social_links = site.get("social_links", [])

    links_by_key: dict[str, dict[str, object]] = {}
    for link in social_links:
        label = str(link.get("label", ""))
        if not label:
            continue
        links_by_key[_social_key(label)] = link

    contact_quick_links = site.get("contact", {}).get("quick_links", {})

    def social_url(key: str, fallback: str = "#") -> str:
        configured_url = contact_quick_links.get(key)
        if isinstance(configured_url, str) and configured_url.strip():
            return configured_url

        link = links_by_key.get(_social_key(key))
        if isinstance(link, dict):
            resolved_url = link.get("url")
            if isinstance(resolved_url, str) and resolved_url.strip():
                return resolved_url

        return fallback

    def t(key: str, **kwargs: object) -> str:
        return translate(key, current_language, **kwargs)

    def lang_url(endpoint: str, **values: object) -> str:
        values["lang"] = current_language
        return flask.url_for(endpoint, **values)

    return {
        "asset_version": ASSET_VERSION,
        "current_lang": current_language,
        "current_year": datetime.now().year,
        "is_rtl": current_language in RTL_LANGUAGES,
        "lang_url": lang_url,
        "social_url": social_url,
        "site": site,
        "supported_languages": SUPPORTED_LANGUAGES,
        "t": t,
    }


@app.route("/")
def home() -> str:
    return flask.render_template("home.html", page_name="home")


@app.route("/projects")
def projects() -> str:
    return flask.render_template("projects.html", page_name="projects")


@app.route("/projects/case-study")
def case_study() -> str:
    return flask.render_template("case_study.html", page_name="case_study")


@app.route("/resume")
def resume() -> str:
    return flask.render_template("resume.html", page_name="resume")


@app.route("/contact")
def contact() -> str:
    return flask.render_template("contact.html", page_name="contact")


@app.after_request
def add_response_headers(response: flask.Response) -> flask.Response:
    selected_language = normalize_language(getattr(g, "current_language", "en"))
    response.set_cookie(
        "portfolio_lang",
        selected_language,
        max_age=60 * 60 * 24 * 365,
        samesite="Lax",
        httponly=True,
        secure=request.is_secure,
    )

    # Apply strict no-cache headers only to HTML responses to avoid
    # disabling caching for static assets such as CSS/JS/images.
    if response.mimetype == "text/html":
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response
