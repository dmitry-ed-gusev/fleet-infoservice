# coding=utf-8

"""
    Scrapers Abstractions. Define base interface / behavior / properties for all Scrapers.

    Created:  Dmitrii Gusev, 02.05.2021
    Modified: Dmitrii Gusev, 31.05.2021
"""

import logging
from datetime import datetime
from abc import ABC, abstractmethod

SCRAPE_RESULT_OK = "Scraped OK!"

# module logging setup
log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")


class ScraperAbstractClass(ABC):
    """Base Abstract Class for all scrapers. Define base behavior and properties for all scrapers."""

    def __init__(self):
        """Base Constructor for scrapers. Define necessary fields.
        :param source_name:
        :param cache_path:
        """
        log.info("Scraper Abstract Class: initializing.")

    @abstractmethod
    def scrap(self, timestamp: datetime, dry_run: bool, requests_limit: int = 0) -> str:
        """Abstract method to be overridden by subclasses.
        :param dry_run: dry run -> true/false, default = false (each run is real, not 'dry').
            If dry run = True, requests_limit parameter will be ignored.
        :param requests_limit: limit for performed HTTP requests to the source system, default = 0 (no limit).
            Any value <= 0 - no limit.
        :return: text message - scrap result
        """
        pass
