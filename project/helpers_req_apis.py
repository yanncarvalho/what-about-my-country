# -*- coding: utf-8 -*-
from http import client
from http.client import HTTPSConnection
import json
import logging

def _get_endpoint_wbank_itens_amount(conn: HTTPSConnection, request: str, http_method: str = 'GET') -> int:
    """Access the World bank API and the number of elements in a specific endpoint"""
    conn.request(http_method, f"/{request}?format=Json&per_page=1")
    response = conn.getresponse()
    data = json.loads(response.read().decode())
    return data[0]['total']

def get_items_wbank_api(urlBaseApiHttps: str, requests: list, http_method: str = 'GET') -> list:
    """ Access the World Bank API and return a tuple with request data at first element are data requited and second one is the last update of the API"""
    conn = client.HTTPSConnection(urlBaseApiHttps)
    result: list = []
    for req in requests:
        per_page = _get_endpoint_wbank_itens_amount(conn, req, http_method)
        conn.request(http_method, f"/{req}?format=Json&per_page={per_page}")
        response = conn.getresponse()
        json_resp = json.loads(response.read().decode())
        data = json_resp[1]
        logging.info(
            " get world bank information from country iso2code ", req)
        result += data
    conn.close()
    return result


