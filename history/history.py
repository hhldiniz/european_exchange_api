import json
from typing import Optional, Any

from logger import Logger
from repository.currency_repository import CurrencyRepository
from terraform.project_dependencies.common.python.util.response import Response, ResponseCodes, CommonHeaders
from terraform.project_dependencies.history.action import Action
from util.json_encoder import MyJsonEncoder


def get_history_lambda_handler(event: dict, context: Optional[dict]) -> dict[str, Any]:
    try:
        action: str = event["action"].upper()
        headers = {CommonHeaders.ContentType.value: "application/json"}
        ok_response_code = ResponseCodes.Status200.value[0]
        if action == Action.HISTORY.name:
            return Response(status_code=ok_response_code, headers=headers, body=get_currency_history()).to_dict()
        elif action == Action.LATEST.name:
            return Response(status_code=ok_response_code, headers=headers, body=get_currency_latest()).to_dict()
        else:
            return Response(status_code=ResponseCodes.Status400.value[0], headers={}, body="BAD REQUEST").to_dict()
    except ValueError as e:
        return Response(status_code=ResponseCodes.Status400.value[0], headers={}, body=e.__str__()).to_dict()
    except Exception as e:
        return Response(status_code=ResponseCodes.Status500.value[0], headers={}, body=e.__str__()).to_dict()


def get_currency_history() -> str:
    Logger.i("Request /history")
    start_at = request.args.get('start_at')
    end_at = request.args.get('end_at')
    base = request.args.get('base')
    symbols = request.args.get('symbols').split(',') if 'symbols' in request.args.keys() else None
    currency_repository = CurrencyRepository()

    return json.dumps(currency_repository.get_all(base, start_at, end_at, symbols), cls=MyJsonEncoder)


def get_currency_latest() -> str:
    Logger.i("Request /latest")
    Logger.i(f"Params: {request.args}")
    symbol = request.args.get("symbol")
    if symbol is None:
        raise ValueError("Missing argument")
    currency_repository = CurrencyRepository()
    return json.dumps(currency_repository.get_latest(symbol), cls=MyJsonEncoder)
