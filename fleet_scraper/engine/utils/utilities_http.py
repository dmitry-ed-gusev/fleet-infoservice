# coding=utf-8

"""
    HTTP / network related utilities module for Fleet DB Scraper.

    Useful resources:
        - (download file) https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3

    Created:  Dmitrii Gusev, 01.06.2021
    Modified: Dmitrii Gusev, 01.06.2021
"""

import ssl
import logging
from urllib import request, parse

from . import constants as const

# init module logger
log = logging.getLogger(const.LOGGING_UTILITIES_HTTP_LOGGER)


# todo: add perform_http_get_request() method + appropriately rename the method below
def perform_http_get_request(url: str) -> str:  # todo: refactor - generalize
    """"""
    # log.debug()  # <- too much output

    if url is None or len(url.strip()) == 0:  # fail-fast - empty URL
        raise ValueError('Provided empty URL, can\'t perform the request!')
    # todo: implementation!
    return ''


def perform_http_post_request(url: str, request_params: dict) -> str:
    """Perform one HTTP POST request with one form parameter for search.
    :return: HTML output with found data
    """
    # log.debug('perform_request(): request param [{}].'.format(request_param))  # <- too much output

    if url is None or len(url.strip()) == 0:  # fail-fast - empty URL
        raise ValueError('Provided empty URL, can\'t perform the request!')

    data = parse.urlencode(request_params).encode(const.DEFAULT_ENCODING)  # perform encoding of request
    req = request.Request(url, data=data)  # this will make the method "POST" request (with data load)
    context = ssl.SSLContext()  # new SSLContext -> to bypass security certificate check
    response = request.urlopen(req, context=context)  # perform request itself

    return response.read().decode(const.DEFAULT_ENCODING)  # read response and perform decode


def download_file_over_http(url: str, target_file: str):
    """"""
    pass