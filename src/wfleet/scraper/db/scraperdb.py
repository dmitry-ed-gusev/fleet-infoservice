#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Fleet Scraper DB main module. Facade for DB operations.

    Created:  Dmitrii Gusev, 23.07.2022
    Modified: Dmitrii Gusev, 30.07.2022

"""

from datetime import datetime
from abc import ABCMeta, abstractclassmethod
from wfleet.scraper.config.scraper_messages import MSG_MODULE_ISNT_RUNNABLE


class AbstractScraperDB(metaclass=ABCMeta):
    """
    Abstract Scraper DB class with the list of necessary methods (Scraper DB interface).
    This class should be implemented (inherited) by concrete DB-related classes.
    """

    @abstractclassmethod
    def add_scraper_telemetry(self, start: datetime, end: datetime, params: str) -> int:
        pass

    @abstractclassmethod
    def get_scraper_telemetry(self) -> None:
        pass

    @abstractclassmethod
    def add_base_ship(self):
        pass

    @abstractclassmethod
    def get_base_ships(self):
        pass


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
