from typing import Any, Optional

import requests

import constants

from logger import Logger

def get_currencies_lambda_handler(event: dict, context: Optional[dict])-> dict[str, Any]:
    return get_currencies(event, context)


def get_currencies(event: dict, context: Optional[dict]) -> dict[str, Any]:
    Logger.d("Passed event: %s", event)
    if context:
        Logger.i("Passed context: %s", context)
    currency_list_res = requests.get(url=constants.currencies_url)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {
            "currencies ": str(currency_list_res.content, "utf-8")
        }
    }
