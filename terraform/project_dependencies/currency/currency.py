from typing import Any, Optional

import requests

from python import constants

from logger import Logger
from util.response import Response, CommonHeaders


def get_currencies_lambda_handler(event: dict, context: Optional[dict]) -> dict[str, Any]:
    return get_currencies(event, context)


def get_currencies(event: dict, context: Optional[dict]) -> dict[str, Any]:
    Logger.d("Passed event: %s", event)
    if context:
        Logger.i("Passed context: %s", context)
    currency_list_res = requests.get(url=constants.currencies_url)
    headers = {
        CommonHeaders.ContentType.value: "application/json"
    }
    body = {
        "currencies ": str(currency_list_res.content, "utf-8")
    }
    return Response(status_code=200, headers=headers, body=body).to_dict()
