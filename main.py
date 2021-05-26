import os

from waitress import serve
from flask import Flask

from config import Config
from currency.currency import currency_bp
from history.history import history_bp
from login.login import login_bp

if __name__ == "__main__":
    app = Flask("__name__", static_folder="static")
    app.register_blueprint(currency_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(login_bp)
    if Config.SERVER_ENV == "TEST":
        app.run("localhost", 8080)
    else:
        serve(app, host='0.0.0.0', port=80)
