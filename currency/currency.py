import requests
import constants

def get_currencies(event: dict, context: dict) -> bytes:
    currency_list_res = requests.get(url=constants.currencies_url)
    return currency_list_res.content

