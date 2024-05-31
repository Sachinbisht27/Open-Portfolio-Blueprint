from flask import Flask
from typing import Type

app: Type[Flask] = Flask(__name__)

from .views import *

if __name__ == "__main__":
    app.run()
