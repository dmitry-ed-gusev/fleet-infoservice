#!/usr/bin/env python3
# coding=utf-8

"""
    Sea Web main module.
    Main data source address is https://maritime.ihs.com

    Created:  Gusev Dmitrii, 04.05.2022
    Modified: Gusev Dmitrii, 04.05.2022
"""

import logging
from datetime import datetime
from wfleet.scraper.engine.imo_processor import get_imo_numbers
from wfleet.scraper.engine.scrapers.seaweb.scraper_seaweb import scrap_base_ships_data
from wfleet.scraper.engine.scrapers.seaweb.scraper_seaweb import scrap_extended_ships_data
# from wfleet.scraper.engine.scrapers.seaweb.parser_seaweb import parse_all_ships
from wfleet.scraper.config.scraper_config import Config, MSG_MODULE_ISNT_RUNNABLE
from wfleet.scraper.engine.scraper_abstract import ScraperAbstractClass, SCRAPE_RESULT_OK

log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")


class SeawebScraper(ScraperAbstractClass):
    """Scraper for maritime.ihs.com source system (Sea Web)."""

    def __init__(self):
        log.info("SeawebScraper: initializing.")

    def scrap(self, timestamp: datetime, dry_run: bool, requests_limit: int = 0) -> str:
        """Sea Web data scraper."""
        log.info("scrap(): processing maritime.ihs.com")

        if dry_run:  # dry run mode - won't do anything!
            return SCRAPE_RESULT_OK

        # scrap base ships data
        scrap_base_ships_data(get_imo_numbers(), req_limit=requests_limit)
        log.debug("Base ships data scraped.")

        # scrap extended ships data
        scrap_extended_ships_data(get_imo_numbers(), req_limit=requests_limit)
        log.debug("Extended ships data scraped.")

        return SCRAPE_RESULT_OK

    def parse(self, dry_run: bool, requests_limit: int = 0):
        """Sea Web data parser."""
        log.info("parse(): processing maritime.ihs.com.")

        if dry_run:  # dry run mode - won't do anything!
            return SCRAPE_RESULT_OK

        return SCRAPE_RESULT_OK


if __name__ == '__main__':
    print(MSG_MODULE_ISNT_RUNNABLE)
