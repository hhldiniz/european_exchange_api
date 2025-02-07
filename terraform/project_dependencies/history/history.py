import json
from typing import Optional, Any, List

from action import Action
from repository.currency_repository import CurrencyRepository
from util.json_encoder import MyJsonEncoder
from util.response import CommonHeaders, ResponseCodes, Response


def get_history_lambda_handler(event: dict, _: Optional[dict]) -> dict[str, Any]:
    try:
        print(f"Params: {event}")
        action: str = event["action"].upper()
        headers = {CommonHeaders.ContentType.value: "application/json"}
        ok_response_code = ResponseCodes.Status200.value[0]
        start_at = event['start_at']
        end_at = event['end_at']
        base = event['base']
        symbols = event['symbols'].split(',') if 'symbols' in event.keys() else None
        if action == Action.HISTORY.name:
            body = get_currency_history(base=base, start_at=start_at, end_at=end_at, symbols=symbols)
            return Response(status_code=ok_response_code, headers=headers, body=body).to_dict()
        elif action == Action.LATEST.name:
            body = get_currency_latest(symbol=symbols)
            return Response(status_code=ok_response_code, headers=headers, body=body).to_dict()
        else:
            return Response(status_code=ResponseCodes.Status400.value[0], headers={}, body="BAD REQUEST").to_dict()
    except ValueError as e:
        return Response(status_code=ResponseCodes.Status400.value[0], headers={},
                        body=f"{type(e).__name__}: {str(e)}").to_dict()
    except KeyError as e:
        return Response(status_code=ResponseCodes.Status400.value[0], headers={},
                        body=f"{e}: Could not read key from dict. Available keys in event are {event.keys()}").to_dict()
    except Exception as e:
        return Response(status_code=ResponseCodes.Status500.value[0], headers={},
                        body=f"{type(e).__name__}: {str(e)}.\n Passed attributes: {event}").to_dict()


def get_currency_history(base: str, start_at: Optional[str], end_at: Optional[str],
                         symbols: Optional[List[str]]) -> str:
    print("Request /history")
    currency_repository = CurrencyRepository()
    return json.dumps(currency_repository.get_all(base, start_at, end_at, symbols), cls=MyJsonEncoder)


def get_currency_latest(symbol: str) -> str:
    print("Request /latest")
    if symbol is None:
        raise ValueError("Missing argument")
    currency_repository = CurrencyRepository()
    return json.dumps(currency_repository.get_latest(symbol), cls=MyJsonEncoder)
