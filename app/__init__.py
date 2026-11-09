from flask import Flask

app = Flask(__name__)

from . import views  # noqa: E402,F401

if __name__ == "__main__":
    app.run(debug=True)
