import flask, random, time
from app import app


@app.route("/")
def hello_world():
    return flask.render_template(
        "home.html", cache_buster=random.random(), time=time
    )

@app.after_request
def add_cache_control(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
