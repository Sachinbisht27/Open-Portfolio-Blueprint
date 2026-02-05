import flask
import random
import time
from app import app


@app.route("/")
def home():
    return flask.render_template("home.html", cache_buster=random.random(), time=time)


@app.route("/projects")
def projects():
    return flask.render_template("projects.html", cache_buster=random.random(), time=time)


@app.route("/projects/dost")
def project_dost():
    return flask.render_template("project_dost.html", cache_buster=random.random(), time=time)


@app.route("/resume")
def resume():
    return flask.render_template("resume.html", cache_buster=random.random(), time=time)


@app.route("/contact")
def contact():
    return flask.render_template("contact.html", cache_buster=random.random(), time=time)


@app.after_request
def add_cache_control(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
