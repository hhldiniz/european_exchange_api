import requests
from flask import Blueprint, Response

import constants

currency_bp = Blueprint("currency", __name__, "static")


@currency_bp.route("/currencies", methods=["GET"])
def get_currencies():
    currency_list_res = requests.get(url=constants.currencies_url)
    return Response(currency_list_res.content, content_type="text/xml")


@currency_bp.route("/latest")
def get_latest():
    currency_data = requests.get(url="https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml")
