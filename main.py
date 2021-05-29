from waitress import serve
from flask import Flask

from config import Config
from currency.currency import currency_bp
from history.history import history_bp
from login.login import login_bp

app = Flask("__name__", static_folder="static")

if __name__ == "__main__":
    app.register_blueprint(currency_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(login_bp)
    if Config.SERVER_ENV.value == "TEST":
        app.run("localhost", 8080)
    else:
        serve(app, port=Config.PORT.value)
