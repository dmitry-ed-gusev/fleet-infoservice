#!/usr/bin/env python3
# coding=utf-8

"""
    Scraper for Russian Maritime Register of Shipping Register Book.

    Main data source (source system address): https://rs-class.org/

    Useful materials and resources:
      - ???

    Created:  Gusev Dmitrii, 10.01.2021
    Modified: Gusev Dmitrii, 30.05.2021
"""

import logging
import ssl
import concurrent.futures
import requests
import threading
import time
from urllib import request, parse
from bs4 import BeautifulSoup

from .utils.utilities import build_variations_list, generate_timed_filename
from .utils.utilities_xls import save_base_ships_2_excel, save_extended_ships_2_excel, process_scraper_dry_run
from .utils import constants as const
from .scraper_abstract import ScraperAbstractClass, SCRAPE_RESULT_OK
from .entities.ships import BaseShipDto

# todo: implement unit tests for this module!

# useful constants / configuration
MAIN_URL = "https://lk.rs-class.org/regbook/regbookVessel?ln=ru"
FORM_PARAM = "namer"
ERROR_OVER_1000_RECORDS = "Результат запроса более 1000 записей! Уточните параметры запроса"

# 10 workers -> 650 sec on my Mac
# 20 workers -> 409 sec on my Mac
# 40 workers -> 323 sec on my Mac
# 100 workers -> 304 sec on my Mac
WORKERS_COUNT = 30  # workers (threads) count for multi-threaded scraping

# module logging setup
log = logging.getLogger(const.SYSTEM_RSCLASSORG)

# setup for multithreading processing
thread_local = threading.local()  # thread local storage
futures = []  # list to store future results of threads


def get_session():
    """Return local thread attribute - http session."""
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def perform_request(request_param: str) -> str:
    """Perform one HTTP POST request with one form parameter for search.
    :return: HTML output with found data
    """
    # log.debug('perform_request(): request param [{}].'.format(request_param))  # <- too much output

    if request_param is None or len(request_param.strip()) == 0:  # fail-fast - empty value
        raise ValueError('Provided empty value [{}]!'.format(request_param))

    my_dict = {FORM_PARAM: request_param}  # dictionary for POST request
    data = parse.urlencode(my_dict).encode(const.DEFAULT_ENCODING)  # perform encoding of request
    req = request.Request(MAIN_URL, data=data)  # this will make the method "POST" request
    context = ssl.SSLContext()  # new SSLContext -> to bypass security certificate check
    response = request.urlopen(req, context=context)  # perform request itself

    return response.read().decode(const.DEFAULT_ENCODING)  # read response and perform decode


def parse_data(html: str) -> dict:
    """Parse HTML with one search request results and return dictionary of BaseShipDto instances (found ships).
    As a dictionary key we use tuple (imo_number, proprietary_number). Proprietary number = register number.
    :return: dictionary with ships parsed from HTML response
    """
    # log.debug('parse_data(): processing.')  # <- too much output

    if not html:  # empty html response provided - return empty dictionary
        log.error("Got empty HTML response - returns empty dictionary!")
        return {}

    if ERROR_OVER_1000_RECORDS in html:
        log.error("Found over 1000 records - returns empty dictionary!")
        return {}

    soup = BeautifulSoup(html, "html.parser")
    table_body = soup.find("tbody", {"id": "myTable0"})  # find <tbody> tag - table body

    ships_dict = {}  # resulting dictionary with Ships

    if table_body:
        table_rows = table_body.find_all('tr')  # find all rows <tr> inside a table body
        # log.debug("Found row(s): {}".format(len(table_rows)))

        for row in table_rows:  # iterate over all found rows
            # log.debug("Processing row: [{}]".format(row))  # <- too much output

            if row:  # if row is not empty - process it
                cells = row.find_all('td')  # find all cells in the table row <tr>

                # get base ship parameters (identity / key)
                imo_number = cells[5].text  # get tag content (text value)
                proprietary_number = cells[4].text  # get tag content (text value)

                # create base ship class instance
                ship: BaseShipDto = BaseShipDto(imo_number, proprietary_number, const.SYSTEM_RSCLASSORG)

                # fill in the main value for base ship
                ship.flag = cells[0].img['title']  # get attribute 'title' of tag <img>
                ship.main_name = cells[1].contents[0]  # get 0 element fro the cell content
                ship.secondary_name = cells[1].div.text  # get value of the tag <div> inside the cell
                ship.home_port = cells[2].text  # get tag content (text value)
                ship.call_sign = cells[3].text  # get tag content (text value)
                ship.extended_info_url = '-'  # todo: implement parsing this value

                # put ship into dictionary
                ships_dict[(imo_number, proprietary_number)] = ship

    return ships_dict


def perform_one_request(search_string: str) -> dict:
    """Perform one request to RSCLASS.ORG and parse the output."""
    ships = parse_data(perform_request(search_string))
    log.info("Found ship(s): {}, search string: {}".format(len(ships), search_string))
    return ships


def perform_ships_search_single_thread(symbols_variations: list) -> dict:
    """Process list of strings for the search in single thread.
    :param symbols_variations: symbols variations for search
    :return: ships dictionary for the given list of symbols variations
    """
    log.debug("perform_ships_search_single_thread(): perform single-threaded search.")

    if symbols_variations is None or not isinstance(symbols_variations, list):
        raise ValueError(f'Provided empty list [{symbols_variations}] or it isn\'t a list!')

    local_ships = {}  # result of the ships search
    counter = 1

    variations_length = len(symbols_variations)

    for search_string in symbols_variations:
        log.debug(f"Currently processing: {search_string} ({counter} out of {variations_length})")
        ships = perform_one_request(search_string)  # request and get HTML + parse received data + get ships dict
        local_ships.update(ships)  # update main dictionary with found data
        log.info(f"Found ship(s): {len(ships)}, total: {len(local_ships)}, search string: {search_string}")
        counter += 1  # increment counter

    return local_ships


def perform_ships_search_multiple_threads(symbols_variations: list, workers_count: int) -> dict:
    """Process list of strings for the search in multiple threads.
    :param symbols_variations: symbols variations for search
    :param workers_count:
    :return: ships dictionary for the given list of symbols variations
    """
    log.debug("perform_ships_search_multiple_threads(): perform multi-threaded search.")

    if symbols_variations is None or not isinstance(symbols_variations, list):  # fail-fast - check input params
        raise ValueError(f'Provided empty list [{symbols_variations}] or it isn\'t a list!')

    if workers_count < 2:  # fail-fast - check workers count
        raise ValueError('Provided workers count < 2, use single-threaded function!')

    local_ships = {}  # result of the ships search

    # run processing in multiple threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers_count) as executor:
        for symbol in symbols_variations:
            future = executor.submit(perform_one_request, symbol)
            futures.append(future)

        # directly loop over futures to wait for them in the order they were submitted
        for future in futures:
            result = future.result()
            local_ships.update(result)

        log.info(f"Found total ships: {len(local_ships)}.")

        return local_ships


class RsClassOrgScraper(ScraperAbstractClass):
    """Scraper for rs-class.org source system."""

    def __init__(self, source_name: str, cache_path: str):
        super().__init__(source_name, cache_path)
        self.log = logging.getLogger(const.SYSTEM_RSCLASSORG)
        self.log.info(f'RsClassOrgScraper: source name {self.source_name}, cache path: {self.cache_path}.')

    def scrap(self, dry_run: bool = False):
        """RS Class Org data scraper."""
        log.info("scrap(): processing rs-class.org")

        if dry_run:  # dry run mode - won't do anything!
            process_scraper_dry_run(const.SYSTEM_RSCLASSORG)
            return SCRAPE_RESULT_OK

        main_ships: dict = {}  # ships search result

        # build list of variations for search strings + measure time
        start_time = time.time()
        variations = build_variations_list()
        self.log.debug(f'Built variations [{len(variations)}] in {time.time() - start_time} second(s).')

        try:
            # process all generated variations strings + measure time - multi-/single-threaded processing
            start_time = time.time()
            if WORKERS_COUNT <= 1:  # single-threaded processing
                self.log.info("Processing mode: [SINGLE THREADED].")
                main_ships.update(perform_ships_search_single_thread(variations))
            else:
                self.log.info("Processing mode: [MULTI THREADED].")
                main_ships.update(perform_ships_search_multiple_threads(variations, WORKERS_COUNT))
            scrap_duration = time.time() - start_time
            log.info(f"Found total ship(s): {len(main_ships)} in {scrap_duration} seconds.")
        except ValueError as err:  # value error
            return f"Value error: {err}"
        except Exception:  # default case - any unexpected error
            import sys
            print("Unexpected error:", sys.exc_info()[0])
            raise

        # path to cache directory for the current scraper run
        xls_path: str = self.cache_path + '/' + generate_timed_filename(self.source_name) + '/'

        # save base ships info
        xls_base_file = xls_path + const.EXCEL_BASE_SHIPS_DATA
        save_base_ships_2_excel(list(main_ships.values()), xls_base_file)
        log.info(f"Saved base ships info to file {xls_base_file}")

        # save extended ships info
        xls_extended_file = xls_path + const.EXCEL_EXTENDED_SHIPS_DATA
        save_extended_ships_2_excel(list({}.values()), xls_extended_file)
        log.info(f"Saved extended ships info to file {xls_extended_file}")

        return SCRAPE_RESULT_OK


# main part of the script
if __name__ == '__main__':
    print('Don\'t run this script directly! Use wrapper script!')
