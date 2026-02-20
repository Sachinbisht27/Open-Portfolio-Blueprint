from __future__ import annotations

from datetime import datetime
import random

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

    def t(key: str, **kwargs: object) -> str:
        return translate(key, current_language, **kwargs)

    def lang_url(endpoint: str, **values: object) -> str:
        values["lang"] = current_language
        return flask.url_for(endpoint, **values)

    return {
        "cache_buster": random.random(),
        "current_lang": current_language,
        "current_year": datetime.now().year,
        "is_rtl": current_language in RTL_LANGUAGES,
        "lang_url": lang_url,
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


@app.route("/projects/dost")
def project_dost() -> str:
    return flask.render_template("project_dost.html", page_name="project_dost")


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
