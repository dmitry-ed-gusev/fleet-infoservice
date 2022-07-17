#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Scraper for Vessel Finder ships storage / site.
    Main data source: https://www.vesselfinder.com/

    Useful materials and resources:
      - ???

    Created:  Dmitrii Gusev, 29.05.2021
    Modified: Dmitrii Gusev, 29.03.2022
"""

# todo: implement the module content (scraping)!
# todo: implement unit tests for this module!

import logging
import warnings
from datetime import datetime
from wfleet.scraper.config.scraper_config import MSG_MODULE_ISNT_RUNNABLE
from wfleet.scraper.engine.scraper_abstract import ScraperAbstractClass, SCRAPE_RESULT_OK


# module logging setup
# log = logging.getLogger(const.SYSTEM_VESSELFINDERCOM)
log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")


class VesselFinderComScraper(ScraperAbstractClass):
    """Scraper for vesselfinder.com source system."""

    def __init__(self):
        log.info("VesselFinderComScraper: initializing.")

    def scrap(self, timestamp: datetime, dry_run: bool, requests_limit: int = 0):
        """Vesselfinder data scraper."""

        log.info("scrap(): processing vesselfinder.com")

        # not implemented warning
        warnings.warn("This module is not implemented yet!", Warning, stacklevel=2)

        if dry_run:  # dry run mode - won't do anything!
            return SCRAPE_RESULT_OK

        return SCRAPE_RESULT_OK


# main part of the script
if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
