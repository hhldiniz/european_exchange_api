from flask import Flask

from currency.currency import currency_bp
from history.history import history_bp
from login.login import login_bp

app = Flask("__name__", static_folder="static")

if __name__ == "__main__":
    app.register_blueprint(currency_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(login_bp)
    app.run("localhost", 8080)

