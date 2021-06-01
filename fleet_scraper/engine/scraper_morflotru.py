#!/usr/bin/env python3
# coding=utf-8

"""
    Scraper for Morflot Ships Book.

    Main data source (source system address): http://morflot.gov.ru/

    Useful materials and resources:
      - (excel) http://morflot.gov.ru/deyatelnost/transportnaya_bezopasnost/reestryi/reestr_obyektov_i_transportnyih_sredstv/f3926.html
      - (direct link to excel) http://morflot.gov.ru/files/docslist/3926-6154-ts_razdel_3.xlsx

    Created:  Dmitrii Gusev, 29.05.2021
    Modified: Dmitrii Gusev, 01.06.2021
"""

import logging
import shutil
from pathlib import Path
from urllib import request

from .utils import constants as const
from .utils.utilities import generate_timed_filename
from .utils.utilities_xls import process_scraper_dry_run
from .scraper_abstract import ScraperAbstractClass, SCRAPE_RESULT_OK
from .entities.ships import BaseShipDto

# todo: implement unit tests for this module!

MORFLOT_DATA_URL = 'http://morflot.gov.ru/files/docslist/3926-6154-ts_razdel_3.xlsx'

# module logging setup
log = logging.getLogger(const.SYSTEM_MORFLOTRU)


class MorflotRuScraper(ScraperAbstractClass):
    """Scraper for morflot.ru source system."""

    def __init__(self, source_name: str, cache_path: str):
        super().__init__(source_name, cache_path)
        self.log = logging.getLogger(const.SYSTEM_MORFLOTRU)
        self.log.info(f'MorflotRuScraper: source name {self.source_name}, cache path: {self.cache_path}.')

    def scrap(self, dry_run: bool = False, requests_limit: int = 0):
        """Morflot data scraper."""
        log.info("scrap(): processing rivreg.ru")

        if dry_run:  # dry run mode - won't do anything!
            process_scraper_dry_run(const.SYSTEM_MORFLOTRU)
            return SCRAPE_RESULT_OK

        # todo: extract the following file download into separated method
        # generate scraper cache directory path + create necessary dir(s)
        scraper_cache_dir: str = self.cache_path + '/' + generate_timed_filename(self.source_name) + '/'
        Path(scraper_cache_dir).mkdir(parents=True, exist_ok=True)  # create necessary parent dirs in path
        self.log.debug(f'Created scraper cache dir: {scraper_cache_dir}.')

        # get raw data in excel format from River Register site and save to cache dir
        raw_file_name: str = scraper_cache_dir + Path(MORFLOT_DATA_URL).name
        self.log.debug(f'Generated raw file name: {raw_file_name}.')
        # download the file from the provided `url` and save it locally under certain `file_name`:
        with request.urlopen(MORFLOT_DATA_URL) as response, open(raw_file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        self.log.info(f'Downloaded raw data file: {MORFLOT_DATA_URL}.')

        # parse data into target format (base + extended excel files)
        # todo: implementation

        return SCRAPE_RESULT_OK

# main part of the script
if __name__ == '__main__':
    print('Don\'t run this script directly! Use wrapper script!')
