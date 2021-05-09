import json

from flask import Blueprint, request

from repository.currency_repository import CurrencyRepository

history_bp = Blueprint("history", __name__, static_folder="static")


@history_bp.route("/history")
def get_currency_history():
    start_at = request.args.get('start_at')
    end_at = request.args.get('end_at')
    base = request.args.get('base')
    symbol = request.args.get('symbol')
    currency_repository = CurrencyRepository()

    return json.dumps(currency_repository.get_all())
