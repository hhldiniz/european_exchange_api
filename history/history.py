import os.path

from flask import Blueprint, request, Response
from requests import get
import xml.etree.ElementTree as elementTree

import constants

history_bp = Blueprint("history", __name__, static_folder="static")


@history_bp.route("/history")
def get_currency_history():
    start_at = request.args.get('start_at')
    end_at = request.args.get('end_at')
    base = request.args.get('base')
    symbol = request.args.get('symbol')
    xml_file_path = os.path.join(constants.APP_ROOT, "history/static/content.xml")
    try:
        xml_file = open(xml_file_path, "r")
    except FileNotFoundError:
        xml_file = open(xml_file_path, "w")
        res = get(constants.history_all_time_url)
        xml_file.write(res.content.decode("utf-8"))
    xml = elementTree.parse(xml_file)
    return Response(xml.getroot().text.text, content_type="text/xml")
