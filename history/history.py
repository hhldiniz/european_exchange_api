import json
from flask import Blueprint, request

from logger import Logger
from repository.currency_repository import CurrencyRepository
from util.json_encoder import MyJsonEncoder

history_bp = Blueprint("history", __name__, static_folder="static")


@history_bp.route("/history")
def get_currency_history():
    Logger.i("Request /history")
    start_at = request.args.get('start_at')
    end_at = request.args.get('end_at')
    base = request.args.get('base')
    symbols = request.args.get('symbols').split(',') if 'symbols' in request.args.keys() else None
    currency_repository = CurrencyRepository()

    return json.dumps(currency_repository.get_all(base, start_at, end_at, symbols), cls=MyJsonEncoder)


@history_bp.route("/latest")
def get_currency_latest():
    Logger.i("Request /latest")
    Logger.i(f"Params: {request.args}")
    symbol = request.args.get("symbol")
    if symbol is None:
        return json.dumps({"error": "Missing argument"}), 400
    currency_repository = CurrencyRepository()
    return json.dumps(currency_repository.get_latest(symbol), cls=MyJsonEncoder)
