# coding=utf-8

"""
    HTTP / network related utilities module for Fleet DB Scraper.

    Useful resources:
        - (download file) https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3

    Created:  Dmitrii Gusev, 01.06.2021
    Modified: Dmitrii Gusev, 16.06.2021
"""

import ssl
import logging
import shutil
from urllib import request, response, parse, error
from pathlib import Path

from . import constants as const

# init module logger
log = logging.getLogger(const.LOGGING_UTILITIES_HTTP_LOGGER)


# todo: add perform_http_get_request() method + appropriately rename the method below
def perform_http_get_request(url: str) -> str:  # todo: refactor - generalize
    """"""
    # log.debug()  # <- too much output

    if url is None or len(url.strip()) == 0:  # fail-fast - empty URL
        raise ValueError("Provided empty URL, can't perform the request!")
    # todo: implementation!
    return ""


def perform_http_post_request(url: str, request_params: dict, retry_count: int = 0) -> str:
    """Perform one HTTP POST request with one form parameter for search.
    :param url:
    :param request_params:
    :param retry_count: number of retries. 0 -> no retries (one request), less than 0 -> no requests at all,
                        greater than 0 -> (retry_count + 1) - such number of requests
    :return: HTML output with found data
    """

    if url is None or len(url.strip()) == 0:  # fail-fast - empty URL
        raise ValueError("Provided empty URL, can't perform the request!")

    data = parse.urlencode(request_params).encode(
        const.DEFAULT_ENCODING
    )  # perform encoding of request params
    req = request.Request(url, data=data)  # this will make the method "POST" request (with data load)
    context = ssl.SSLContext()  # new SSLContext -> to bypass security certificate check

    tries_counter: int = 0
    response_ok: bool = False
    my_response = None
    while tries_counter <= retry_count and not response_ok:  # perform specified number of requests
        log.debug(f"HTTP POST: URL: {url}, data: {request_params}, try #{tries_counter}/{retry_count}.")
        try:
            my_response = request.urlopen(req, context=context, timeout=const.TIMEOUT_URLLIB_URLOPEN)
            response_ok = True  # after successfully done request we should stop requests
        except (TimeoutError, error.URLError) as e:
            log.error(
                f"We got error -> URL: {url}, data: {request_params}, try: #{tries_counter}/{retry_count}, "
                f"error: {e}."
            )

        tries_counter += 1

    if my_response is not None:
        result = my_response.read().decode(const.DEFAULT_ENCODING)  # read response and perform decode
    else:
        result = None

    return result


def perform_file_download_over_http(url: str, target_dir: str, target_file: str = None) -> str:
    """Downloads file via HTTP protocol.
    :param url: URL for file download, shouldn't be empty.
    :param target_dir: local dir to save file, if empty - save to the current dir
    :param target_file: local file name to save, if empty - file name will be derived from URL
    :return: path to locally saved file, that was downloaded
    """
    log.debug(
        f"perform_file_download_over_http(): downloading link: {url}, target dir: {target_dir}, "
        f"target_file: {target_file}."
    )

    if url is None or len(url.strip()) == 0:  # fail-fast check for provided url
        raise ValueError("Provided empty URL!")

    # check target dir name - if not empty we will create all missing dirs in the path
    if target_dir is not None and len(target_dir.strip()) > 0:
        Path(target_dir).mkdir(parents=True, exist_ok=True)  # create necessary parent dirs in path
        log.debug(f"Created all missing dirs in path: {target_dir}")
    else:
        log.debug(f"Provided empty target dir - file will be saved in the current directory.")

    # pick a target file name
    if target_file is None or len(target_file.strip()) == 0:
        local_file_name: str = Path(url).name
    else:
        local_file_name: str = target_file
    log.debug(f"Target file name: {local_file_name}")

    # construct the full local target path
    local_path: str = target_dir + "/" + local_file_name
    log.debug(f"Generated local full path: {local_path}")

    # download the file from the provided `url` and save it locally under certain `file_name`:
    with request.urlopen(url) as my_response, open(local_path, "wb") as out_file:
        shutil.copyfileobj(my_response, out_file)
    log.info(f"Downloaded file: {url} and put here: {local_path}")

    return local_path
