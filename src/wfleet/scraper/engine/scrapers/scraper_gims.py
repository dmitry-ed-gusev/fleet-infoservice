#!/usr/bin/env python3
# coding=utf-8

"""
    Scraper for GIMS ships book.

    Main data source (source system address):
      https://www.mchs.gov.ru/ministerstvo/uchrezhdeniya-mchs-rossii/gosudarstvennaya-inspekciya-po-malomernym-sudam

    Useful materials and resources:
      - http://www.gims.ru/ - looks like unofficial web site

    Created:  Dmitrii Gusev, 29.05.2021
    Modified: Dmitrii Gusev, 02.01.2022
"""

import logging
from datetime import datetime
from wfleet.scraper.config.scraper_config import CONFIG, MSG_MODULE_ISNT_RUNNABLE
# from wfleet.scraper.utils.utilities_xls import process_scraper_dry_run
from wfleet.scraper.engine.scraper_abstract import ScraperAbstractClass, SCRAPE_RESULT_OK

# todo: implement unit tests for this module!

# module logging setup
log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")


class GimsRuScraper(ScraperAbstractClass):
    """Scraper for GIMS source system."""

    def __init__(self):
        # super().__init__()
        log.info("GimsRuScraper: initializing.")

    def scrap(self, timestamp: datetime, dry_run: bool, requests_limit: int = 0):
        """GIMS data scraper method."""
        log.info("scrap(): processing GIMS")

        if dry_run:  # dry run mode - won't do anything!
            # process_scraper_dry_run(const.SYSTEM_GIMS)
            return SCRAPE_RESULT_OK


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
