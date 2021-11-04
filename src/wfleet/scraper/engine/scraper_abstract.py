# coding=utf-8

"""
    Scrapers Abstractions. Define base interface / behavior / properties for all Scrapers.

    Created:  Dmitrii Gusev, 02.05.2021
    Modified: Dmitrii Gusev, 31.05.2021
"""

from abc import ABC, abstractmethod

SCRAPE_RESULT_OK = "Scraped OK!"


class ScraperAbstractClass(ABC):
    """Base Abstract Class for all scrapers. Define base behavior and properties for all scrapers."""

    def __init__(self, source_name: str, cache_path: str):
        """Base Constructor for scrapers. Define necessary fields.
        :param source_name:
        :param cache_path:
        """
        self.source_name = source_name
        self.cache_path = cache_path

    @abstractmethod
    def scrap(self, dry_run: bool = False, requests_limit: int = 0) -> str:
        """Abstract method to be overridden by subclasses.
        :param dry_run: dry run -> true/false, default = false (each run is real, not 'dry').
            If dry run = True, requests_limit parameter will be ignored.
        :param requests_limit: limit for performed HTTP requests to the source system, default = 0 (no limit).
            Any value <= 0 - no limit.
        :return: text message - scrap result
        """
        pass
