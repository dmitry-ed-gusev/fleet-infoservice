#!/usr/bin/env python3
# coding=utf-8

"""
    Scraper for River Register Book.

    Main data source (source system address): https://www.rivreg.ru/

    Useful materials and resources:
      - https://www.rivreg.ru/activities/class/regbook/ - register book url (actual data)

    Created:  Gusev Dmitrii, 04.05.2021
    Modified: Dmitrii Gusev, 30.05.2021
"""

import logging

from .utils import constants as const
from .utils.utilities_xls import process_scraper_dry_run
from .scraper_abstract import ScraperAbstractClass, SCRAPE_RESULT_OK
from .entities.ships import BaseShipDto

# todo: implement unit tests for this module!

# module logging setup
log = logging.getLogger(const.SYSTEM_RIVREGRU)


class RivRegRuScraper(ScraperAbstractClass):
    """Scraper for rivreg.ru source system."""

    def __init__(self, source_name: str, cache_path: str):
        super().__init__(source_name, cache_path)
        self.log = logging.getLogger(const.SYSTEM_RIVREGRU)
        self.log.info(f'RivRegRuScraper: source name {self.source_name}, cache path: {self.cache_path}.')

    def scrap(self, dry_run: bool = False):
        """River Register data scraper."""
        log.info("scrap(): processing rivreg.ru")

        if dry_run:  # dry run mode - won't do anything!
            process_scraper_dry_run(const.SYSTEM_RIVREGRU)
            return SCRAPE_RESULT_OK


# main part of the script
if __name__ == '__main__':
    print('Don\'t run this script directly! Use wrapper script!')
