#!/usr/bin/env python3
# coding=utf-8

"""
    Scraper for Vessel Finder ships storage / site.

    Site(s):
        * https://www.vesselfinder.com/ - main url

    Created:  Gusev Dmitrii, 29.04.2021
    Modified: Dmitrii Gusev, 04.05.2021
"""

import logging
from .scraper_interface import ScraperInterface, SCRAPE_RESULT_OK

# useful constants / configuration
LOGGER_NAME = 'scraper_vesselfinder'

# setup logging for the module
log = logging.getLogger(LOGGER_NAME)


def scrap():
    """"""
    log.info("scrap(): processing vesselfinder.com")


class VesselFinderComScraper(ScraperInterface):
    def __init__(self):
        self.log = logging.getLogger(LOGGER_NAME)

    def scrap(self, cache_path: str, workers_count: int, dry_run: bool = False):
        """RS Class Org data scraper."""
        log.info("scrap(): processing rs-class.org")


# main part of the script
if __name__ == '__main__':
    print('Don\'t run this script directly! Use wrapper script!')
