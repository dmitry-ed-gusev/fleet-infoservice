#!/usr/bin/env python3
# coding=utf-8

"""
    Scraper for Russian Maritime Register of Shipping Register Book.

    Main data source (source system address): https://rs-class.org/

    Useful materials and resources:
      - ???

    Created:  Gusev Dmitrii, 10.01.2021
    Modified: Gusev Dmitrii, 21.06.2021
"""

import sys
import time
import logging
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup

from .utils import constants as const
from .utils.utilities import build_variations_list, generate_timed_filename
from .utils.utilities_xls import save_ships_2_excel, process_scraper_dry_run
from .utils.utilities_http import perform_http_post_request
from .scraper_abstract import ScraperAbstractClass, SCRAPE_RESULT_OK
from .entities.ships import ShipDto

# todo: implement unit tests for this module!

# useful constants / configuration
MAIN_URL = "https://lk.rs-class.org/regbook/regbookVessel?ln=ru"
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


def get_session():  # todo: refactor -> move to utility class
    """Return local thread attribute - http session."""
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


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
        table_rows = table_body.find_all("tr")  # find all rows <tr> inside a table body
        # log.debug("Found row(s): {}".format(len(table_rows)))

        for row in table_rows:  # iterate over all found rows
            # log.debug("Processing row: [{}]".format(row))  # <- too much output

            if row:  # if row is not empty - process it
                cells = row.find_all("td")  # find all cells in the table row <tr>

                # get base ship parameters (identity / key)
                imo_number = cells[5].text  # get tag content (text value)
                proprietary_number = cells[4].text  # get tag content (text value)

                # create base ship class instance
                ship: ShipDto = ShipDto(imo_number, proprietary_number, "", const.SYSTEM_RSCLASSORG)

                # fill in the main value for base ship
                ship.flag = cells[0].img["title"]  # get attribute 'title' of tag <img>
                ship.main_name = cells[1].contents[0]  # get 0 element fro the cell content
                ship.secondary_name = cells[1].div.text  # get value of the tag <div> inside the cell
                ship.home_port = cells[2].text  # get tag content (text value)
                ship.call_sign = cells[3].text  # get tag content (text value)
                ship.extended_info_url = "-"  # todo: implement parsing this value

                # put ship into dictionary
                ships_dict[(imo_number, proprietary_number)] = ship

    return ships_dict


def perform_one_request(
    search_string: str,
) -> dict:  # todo: this method is needed for multi-threading - refactor
    """Perform one request to RSCLASS.ORG and parse the output.
    :param search_string:
    :return:
    """
    ships = parse_data(perform_http_post_request(MAIN_URL, {"namer": search_string}, retry_count=5))
    log.info("Found ship(s): {}, search string: {}".format(len(ships), search_string))
    return ships


# todo: merge single-threaded with multi-threaded processing?
def perform_ships_base_search_single_thread(symbols_variations: list, requests_limit: int = 0) -> dict:
    """Process list of strings for the search in single thread.
    :param symbols_variations: symbols variations for search
    :param requests_limit: limit for performed HTTP requests to the source system, default = 0 (no limit).
            Any value <= 0 - no limit.
    :return: ships dictionary for the given list of symbols variations
    """
    log.debug(
        f"perform_ships_base_search_single_thread(): perform single-threaded search. Limit: {requests_limit}."
    )

    if symbols_variations is None or not isinstance(symbols_variations, list):
        raise ValueError(f"Provided empty list [{symbols_variations}] or it isn't a list!")

    local_ships = {}  # result of the ships search
    counter = 1

    variations_length = len(symbols_variations)

    for search_string in symbols_variations:
        log.debug(f"Currently processing: {search_string} ({counter} out of {variations_length})")
        ships = parse_data(
            perform_http_post_request(MAIN_URL, {"namer": search_string})
        )  # HTTP request for base data
        local_ships.update(ships)  # update main dictionary with found data
        log.info(f"Found ship(s): {len(ships)}, total: {len(local_ships)}, search string: {search_string}")

        if 0 < requests_limit <= counter:  # in case limit is set - use it
            return local_ships

        counter += 1  # increment counter

    return local_ships


def perform_ships_base_search_multiple_threads(
    symbols_variations: list, workers_count: int, requests_limit: int = 0
) -> dict:
    """Process list of strings for the search in multiple threads.
    :param symbols_variations: symbols variations for search
    :param workers_count: number of threads for multi-threaded processing
    :param requests_limit: limit for performed HTTP requests to the source system, default = 0 (no limit).
            Any value <= 0 - no limit.
    :return: ships dictionary for the given list of symbols variations
    """
    log.debug("perform_ships_base_search_multiple_threads(): perform multi-threaded search.")

    if symbols_variations is None or not isinstance(
        symbols_variations, list
    ):  # fail-fast - check input params
        raise ValueError(f"Provided empty list [{symbols_variations}] or it isn't a list!")

    if workers_count < 2:  # fail-fast - check workers count
        raise ValueError("Provided workers count < 2, use single-threaded function!")

    local_ships = {}  # result of the ships search

    # run processing in multiple threads
    with ThreadPoolExecutor(max_workers=workers_count) as executor:
        counter = 1
        for symbol in symbols_variations:
            future = executor.submit(perform_one_request, symbol)
            futures.append(future)

            if 0 < requests_limit <= counter:  # in case limit is set - use it
                break

            counter += 1

        # option #1: directly loop over futures to wait for them in the order they were submitted
        # for future in futures:
        #     result = future.result()
        #     local_ships.update(result)

        # option #2: iterate over completed threads and get results
        for task in as_completed(futures):
            result = task.result()
            local_ships.update(result)

        log.info(f"Found total ships: {len(local_ships)}.")

        return local_ships


class RsClassOrgScraper(ScraperAbstractClass):
    """Scraper for rs-class.org source system."""

    def __init__(self, source_name: str, cache_path: str):
        super().__init__(source_name, cache_path)
        self.log = logging.getLogger(const.SYSTEM_RSCLASSORG)
        self.log.info(f"RsClassOrgScraper: source name {self.source_name}, cache path: {self.cache_path}.")

    def scrap(self, dry_run: bool = False, requests_limit: int = 0):
        """RS Class Org data scraper."""
        log.info("scrap(): processing rs-class.org")

        if dry_run:  # dry run mode - won't do anything!
            process_scraper_dry_run(const.SYSTEM_RSCLASSORG)
            return SCRAPE_RESULT_OK

        main_ships: dict = {}  # ships search result

        # build list of variations for search strings + measure time
        start_time = time.time()
        variations = build_variations_list()
        self.log.debug(f"Built variations [{len(variations)}] in {time.time() - start_time} second(s).")

        try:
            # process all generated variations strings + measure time - multi-/single-threaded processing
            start_time = time.time()
            if WORKERS_COUNT <= 1:  # single-threaded processing
                self.log.info("Processing mode: [SINGLE THREADED].")
                main_ships.update(
                    perform_ships_base_search_single_thread(variations, requests_limit=requests_limit)
                )
            else:
                self.log.info("Processing mode: [MULTI THREADED].")
                main_ships.update(
                    perform_ships_base_search_multiple_threads(
                        variations,
                        workers_count=WORKERS_COUNT,
                        requests_limit=requests_limit,
                    )
                )
            scrap_duration = time.time() - start_time
            log.info(f"Found total ship(s): {len(main_ships)} in {scrap_duration} seconds.")
        except ValueError as err:  # value error
            return f"Value error: {err}"
        except Exception:  # default case - any unexpected error
            print("Unexpected error:", sys.exc_info()[0])
            raise

        # path to cache directory for the current scraper run
        if requests_limit > 0:  # mark limited run directory appropriately
            suffix = self.source_name + const.SCRAPER_CACHE_LIMITED_RUN_DIR_SUFFIX
        else:
            suffix = self.source_name
        xls_path: str = self.cache_path + "/" + generate_timed_filename(suffix) + "/"

        # save base ships info
        xls_base_file = xls_path + const.EXCEL_SHIPS_DATA
        save_ships_2_excel(list(main_ships.values()), xls_base_file)
        log.info(f"Saved ships info to file {xls_base_file}")

        return SCRAPE_RESULT_OK


# main part of the script
if __name__ == "__main__":
    print("Don't run this script directly! Use wrapper script!")
