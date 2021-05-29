#!/usr/bin/env python3
# coding=utf-8

"""
    Scraper for Vessel Finder ships storage / site.

    Main data source: https://www.vesselfinder.com/

    Useful materials and resources:
      - ???

    Created:  Dmitrii Gusev, 29.05.2021
    Modified:
"""

import logging

from .utils import constants as const
from .scraper_abstract import ScraperAbstractClass, SCRAPE_RESULT_OK
from .entities.ships import BaseShipDto

# todo: implement unit tests for this module!

# module logging setup
log = logging.getLogger(const.SYSTEM_VESSELFINDERCOM)


class VesselFinderComScraper(ScraperAbstractClass):
    """Scraper for vesselfinder.com source system."""

    def __init__(self, source_name: str, cache_path: str):
        super().__init__(source_name, cache_path)
        self.log = logging.getLogger(const.SYSTEM_VESSELFINDERCOM)
        self.log.info(f'VesselFinderComScraper: source name {self.source_name}, cache path: {self.cache_path}.')

    def scrap(self, dry_run: bool = False):
        """Vesselfinder data scraper."""
        log.info("scrap(): processing vesselfinder.com")

        if dry_run:  # dry run mode - won't do anything!
            self.log.warning("DRY RUN MODE IS ON!")
            return SCRAPE_RESULT_OK


# main part of the script
if __name__ == '__main__':
    print('Don\'t run this script directly! Use wrapper script!')
