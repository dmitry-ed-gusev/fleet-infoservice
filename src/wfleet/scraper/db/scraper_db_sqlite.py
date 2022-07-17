#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Scraper module for SQLite DBMS interaction (pure python).

    See additional resources here:
      - https://habr.com/ru/post/321510/ - pure python
      - https://habr.com/ru/post/322086/ - peewee ORM

    Created:  Dmitrii Gusev, 19.06.2022
    Modified: Dmitrii Gusev, 20.06.2022

"""

import sqlite3
import logging
from wfleet.scraper.config.scraper_config import Config
from wfleet.scraper.utils.utilities import read_file_as_text
from wfleet.scraper.exceptions.scraper_exceptions import ScraperException
from wfleet.scraper.config.scraper_messages import MSG_MODULE_ISNT_RUNNABLE

log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")


class ScraperSQLiteDB:
    """Scraper SQLite DB Class."""

    def __init__(self, db_file: str) -> None:
        log.debug(f'Initializing Scraper SQLite DB in: [{db_file}].')
        if not db_file:
            raise ScraperException("Provided empty DB file!")

        self.__db_file = db_file

    def execute_script(self, script_file: str) -> None:
        log.debug(f'Executing sql script: [{script_file}].')
        if not script_file:
            raise ScraperException('Provided empty script file!')

        # connect to DB
        connection = sqlite3.connect(self.__db_file)
        cursor = connection.cursor()
        log.debug(f"Connected to DB [{self.__db_file}].")
        db_script: str = read_file_as_text(script_file)
        cursor.executescript(db_script)
        # execute script
        # for query in db_script.split(";"):
        #     log.debug(f'Now executing: [{query}].')
        #     cursor.execute(query)
        connection.commit()
        connection.close()

    def add_scraper_run_telemetry(self) -> int:
        pass

    def update_scraper_run_telemetry(self) -> int:
        pass


if __name__ == "__main__":
    # print(MSG_MODULE_ISNT_RUNNABLE)
    config = Config()

    scraper_db = ScraperSQLiteDB(config.db_name)
    scraper_db.execute_script(config.db_schema_file)
