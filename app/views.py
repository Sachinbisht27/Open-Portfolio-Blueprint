import flask
from app import app


@app.route("/")
def hello_world():
    return flask.render_template(
        "home.html",
    )
