#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Scraper module for SQLite DBMS interaction (via PEEWEE ORM).

    See additional resources here:
      - https://habr.com/ru/post/322086/ - peewee ORM
      - http://docs.peewee-orm.com/en/latest/ - peewee ORM docs
      - https://github.com/coleifer/peewee - peewee on GitHub

    Created:  Dmitrii Gusev, 22.06.2022
    Modified: Dmitrii Gusev, 30.07.2022

"""

import sqlite3
import peewee
import logging
from wfleet.scraper.db.scraperdb import AbstractScraperDB
from wfleet.scraper.config.scraper_config import Config
from wfleet.scraper.utils.utilities import read_file_as_text
from wfleet.scraper.exceptions.scraper_exceptions import ScraperException
from wfleet.scraper.config.scraper_messages import MSG_MODULE_ISNT_RUNNABLE

log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")


class ScraperPeweeORM(AbstractScraperDB):
    pass


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
