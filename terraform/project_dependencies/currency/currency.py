from typing import Any, Optional

import requests

import constants
from util.response import Response, CommonHeaders
from util.sns_event_mapping import get_data_from_sns_event


def get_currencies_lambda_handler(event: dict, context: Optional[dict]) -> dict[str, Any]:
    return get_currencies(get_data_from_sns_event(event), context)


def get_currencies(event: dict, context: Optional[dict]) -> dict[str, Any]:
    print("Passed event:", event)
    if context:
        print("Passed context:", context)
    currency_list_res = requests.get(url=constants.currencies_url)
    headers = {
        CommonHeaders.ContentType.value: "application/json"
    }
    body = {
        "currencies ": str(currency_list_res.content, "utf-8")
    }
    return Response(status_code=200, headers=headers, body=body).to_dict()
