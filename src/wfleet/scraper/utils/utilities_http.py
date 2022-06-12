# coding=utf-8

"""
    HTTP / network related utilities module for World Fleet DB Scraper.

    Useful resources:
        - (download file) https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3

    Created:  Dmitrii Gusev, 01.06.2021
    Modified: Dmitrii Gusev, 08.06.2022
"""

import os
import ssl
import logging
import shutil
import requests
from pathlib import Path
from requests import Response
from typing import Dict, Tuple
from urllib import request, parse, error
from wfleet.scraper.config.scraper_config import Config
from wfleet.scraper.exceptions.scraper_exceptions import ScraperException
from wfleet.scraper.config.scraper_messages import MSG_MODULE_ISNT_RUNNABLE

# init module logger
log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")

# timeout for urllib urlopen operation (seconds)
TIMEOUT_URLLIB_URLOPEN = 5

# get application config
config = Config()


class WebClient():
    """Simple WebClient Singleton class (based on [requests] module)."""

    def __init__(self, headers: dict, cookies: dict) -> None:
        log.debug("Initializing WebCLient() singleton instance.")
        self.headers = headers
        self.cookies = cookies
        self.session = requests.Session()

        if headers and len(headers) > 0:  # add headers
            self.session.headers.update(self.headers)
            log.debug("Headers are not empty, adding to the HTTP session.")

        if cookies and len(cookies) > 0:  # add cookies
            self.session.cookies.update(self.cookies)
            log.debug("Cookies are not empty, adding to the HTTP session.")

    def set_redirects_count(self, redirects_count: int):
        if redirects_count > 0:
            self.session.max_redirects = redirects_count

    def get(self, url: str, allow_redirects=True, fail_on_error=True) -> Response:
        log.debug(f"get(): performing get request: [{url}].")

        if not url:
            raise ScraperException("Empty URL for get request!")

        response = self.session.get(url, allow_redirects=allow_redirects)
        if response.status_code != 200 and fail_on_error:  # fail on purpose - by parameter
            raise ScraperException(f"Get request [{url}] failed with [{response.status_code}]!")

        return response

    def get_text(self, url: str, allow_redicrects: bool, fail_on_error: bool) -> str:
        log.debug('get_text(): working.')
        response = self.get(url, allow_redicrects, fail_on_error)
        if response:
            return response.text

        return ''

    def get_text_2_file(self, url: str, file: str, allow_redicrects: bool, fail_on_error: bool) -> None:
        log.debug(f'get_text_2_file(): saving response text to file {file}.')

        if not file or Path(file).exists():
            raise ScraperException(f'File name {file} is empty or file already exists!')

        response_text: str = self.get_text(url, allow_redicrects, fail_on_error)
        if response_text:
            with open(Path(file), 'w') as f:  # write content to the file
                f.write(response_text)
                log.debug(f"Written file: {file}")

    def get_text_2_files(self, urls: Dict[str, str], dir: str, allow_redicrects: bool,
                         fail_on_error: bool) -> None:
        log.debug(f'get_text_2_files(): saving multiple urls to dir: {dir}.')

        if not urls:
            raise ScraperException('Provided empty URLs dictionary!')

        if not dir:
            raise ScraperException('Provided empty dir for saving urls!')

        os.makedirs(dir, exist_ok=True)  # if all is OK - create dir for the ship data

        # check existence of files with additional info and request if missing
        for key in urls:
            file = dir + "/" + key + ".html"
            if not Path(file).exists():  # if file doesn't exist - request it
                # HTTP GET request + save to file
                self.get_text_2_file(urls[key], file, allow_redicrects, fail_on_error)


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

    data = parse.urlencode(request_params).encode(config.encoding)  # perform encoding of request params
    req = request.Request(url, data=data)  # this will make the method "POST" request (with data load)
    context = ssl.SSLContext()  # new SSLContext -> to bypass security certificate check

    tries_counter: int = 0
    response_ok: bool = False
    my_response = None
    while tries_counter <= retry_count and not response_ok:  # perform specified number of requests
        log.debug(f"HTTP POST: URL: {url}, data: {request_params}, try #{tries_counter}/{retry_count}.")
        try:
            my_response = request.urlopen(req, context=context, timeout=TIMEOUT_URLLIB_URLOPEN)
            response_ok = True  # after successfully done request we should stop requests
        except (TimeoutError, error.URLError) as e:
            log.error(
                f"We got error -> URL: {url}, data: {request_params}, try: #{tries_counter}/{retry_count}, "
                f"error: {e}."
            )

        tries_counter += 1

    if my_response is not None:
        result = my_response.read().decode(config.encoding)  # read response and perform decode
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

    if not url or len(url.strip()) == 0:  # fail-fast check for provided url
        raise ValueError("Provided empty URL!")

    # check target dir name - if not empty we will create all missing dirs in the path
    if target_dir is not None and len(target_dir.strip()) > 0:
        Path(target_dir).mkdir(parents=True, exist_ok=True)  # create necessary parent dirs in path
        log.debug(f"Created all missing dirs in path: {target_dir}")
    else:
        log.debug("Provided empty target dir - file will be saved in the current directory.")

    # pick a target file name
    local_file_name: str = ''
    if target_file is None or len(target_file.strip()) == 0:
        local_file_name = Path(url).name
    else:
        local_file_name = target_file
    log.debug(f"Target file name: {local_file_name}")

    # construct the full local target path
    local_path: str = target_dir + "/" + local_file_name
    log.debug(f"Generated local full path: {local_path}")

    # download the file from the provided `url` and save it locally under certain `file_name`:
    with request.urlopen(url) as my_response, open(local_path, "wb") as out_file:
        shutil.copyfileobj(my_response, out_file)
    log.info(f"Downloaded file: {url} and put here: {local_path}")

    return local_path


def process_url(url: str, postfix: str = '', format_values: Tuple[str] = None) -> str:
    log.debug(f'Processing URL [{url}] with postfix [{postfix}] and format values [{format_values}].')

    if not url:
        raise ScraperException('Provided empty URL for processing!')

    processed_url: str = url
    if postfix:  # if postfix - add it to the URL string
        if not processed_url.endswith('/'):
            processed_url += '/'
        processed_url += postfix

    if format_values:  # if there are values - format URL string with them
        processed_url = processed_url.format(*format_values)

    return processed_url


def process_urls(urls: Dict[str, str], postfix: str = '', format_values: Tuple[str] = None) -> Dict[str, str]:
    log.debug('Processing urls dictionary.')

    if not urls:
        raise ScraperException('Provided empty URLs dictionary for processing!')

    processed: Dict[str, str] = dict()
    for key in urls:
        processed[key] = process_url(urls[key], postfix, format_values)

    return processed


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
