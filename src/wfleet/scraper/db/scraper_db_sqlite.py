#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Scraper module for SQLite DBMS interaction (pure python).

    See additional resources here:
      - https://habr.com/ru/post/321510/ - pure python
      - https://habr.com/ru/post/322086/ - peewee ORM
      - https://pynative.com/python-sqlite-date-and-datetime/ - datetime with SQLite
      - https://pynative.com/python-timestamp/ - timestamp examples

    Created:  Dmitrii Gusev, 19.06.2022
    Modified: Dmitrii Gusev, 30.07.2022

"""

import sqlite3
import logging
import time
from datetime import datetime
from sqlite3 import PARSE_DECLTYPES, PARSE_COLNAMES
from wfleet.scraper.db.scraperdb import AbstractScraperDB
from wfleet.scraper.config.scraper_config import Config
from wfleet.scraper.utils.utilities import read_file_as_text
from wfleet.scraper.exceptions.scraper_exceptions import ScraperException
from wfleet.scraper.config.scraper_messages import MSG_MODULE_ISNT_RUNNABLE

log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")


class ScraperSQLiteDB(AbstractScraperDB):
    """Scraper SQLite DB Class."""

    def __init__(self, db_file: str, db_schema_init_file: str = "", init_db: bool = False,
                 db_schema_reset_file: str = "", reset_db: bool = False) -> None:
        log.debug(f'Initializing Scraper SQLite DB in: [{db_file}].')
        if not db_file:
            raise ScraperException("Provided empty DB file!")

        self.__db_file = db_file
        self.__db_schema_init_file = db_schema_init_file
        self.__db_schema_reset_file = db_schema_reset_file

    def execute_update(self, sql: str, data: tuple) -> int:
        """Excute INSERT/UPDATE statements and return last inserted id/nums of rows affected."""

        log.debug(f'Executing SQL: {sql}.')

        if not sql or not (sql.upper().startswith('INSERT') or sql.upper().startswith('UPDATE')):
            raise ScraperException('SQL is empty or is not INSERT/UPDATE!')

        result: int = -1  # result of the operation: lastrowid/# affected rows
        try:
            # connect to DBMS (using internal python type recognition modules)
            connection = sqlite3.connect(self.__db_file, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
            cursor = connection.cursor()
            log.debug(f"Connected to SQLite: {self.__db_file}.")

            # execute the provided sql statement + commit to DB
            cursor.execute(sql, data)
            connection.commit()
            log.debug('Executed SQL statement. '
                      f'Last row ID: {cursor.lastrowid}. '
                      f'Row count: {cursor.rowcount}.')

            if sql.upper().startswith('UPDATE'):
                result = cursor.rowcount
            elif sql.upper().startswith('INSERT'):
                # as [cursor.lastrowid] in sqlite module is Optionl[int] we need this construct
                result = int(0 if cursor.lastrowid is None else cursor.lastrowid)

        except sqlite3.Error as error:  # error handler
            log.error(f"Error while working with SQLite:\n{error}")

        finally:  # in any case we have to close the connection to DB
            if cursor:
                cursor.close()
                log.debug("SQLite cursor is closed.")
            if connection:
                connection.close()
                log.debug("SQLite connection is closed.")

        return result

    def execute_script(self, script_file: str) -> None:
        log.debug(f'Executing sql script: [{script_file}].')
        if not script_file:
            raise ScraperException('Provided empty script file!')

        # connect to DB
        connection = sqlite3.connect(self.__db_file, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
        cursor = connection.cursor()
        log.debug(f"Connected to DB [{self.__db_file}].")
        db_script: str = read_file_as_text(script_file)

        # execute sql script
        cursor.executescript(db_script)

        # execute sql script - statement by statement
        # for query in db_script.split(";"):
        #     log.debug(f'Now executing: [{query}].')
        #     cursor.execute(query)

        connection.commit()
        connection.close()

    def reset_db(self) -> None:
        """Reset DB by executing specified db reset sql file. If file is empty - warn message."""

        log.debug(f"Reset SQLite DB by the script {self.__db_schema_reset_file}.")
        if self.__db_schema_reset_file:
            self.execute_script(self.__db_schema_reset_file)
        else:
            log.warning("No schema reset script specified!")

    def init_db(self) -> None:
        """Init DB by executing specified db schema sql file. If file is empty - warn message."""

        log.debug(f"Initializing SQLite DB by the script {self.__db_schema_init_file}.")
        if self.__db_schema_init_file:
            self.execute_script(self.__db_schema_init_file)
        else:
            log.warning("No schema init script specified!")

    def add_scraper_telemetry(self, start: datetime, end: datetime, params: str) -> int:
        """Adds one Scraper run telemetry to DB."""

        log.debug(f"Add Scraper telemetry -> start: {start}, end: {end}, params: {params}")

        if not start or not end:  # fail-fast if start-end dates are not specified
            raise ScraperException()

        # calculate data
        start_ts = datetime.timestamp(start)
        end_ts = datetime.timestamp(end)
        duration = end_ts - start_ts

        # build sql command and data for it
        sql = """INSERT INTO 'scraper_executions'
                    ('start_timestamp', 'end_timestamp', 'duration', 'parameters')
                    VALUES (?, ?, ?, ?);"""
        data = (start, end, duration, params)

        # execute sql statement
        identity: int = self.execute_update(sql, data)
        log.debug(f'Telemetry entry added successfully. Entry ID = {identity}.')

        return identity

    def get_scraper_telemetry(self) -> None:
        """Return Scraper runs telemetry from DB."""

        log.debug("Return Scraper telemetry.")

        sql = """SELECT * FROM 'scraper_executions'"""

        try:
            # connect to DBMS (using internal python type recognition modules)
            connection = sqlite3.connect(self.__db_file, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
            cursor = connection.cursor()
            log.debug(f"Connected to SQLite: {self.__db_file}.")

            # execute the provided sql statement + commit to DB
            cursor.execute(sql)
            result = cursor.fetchall()
            log.debug(f'Executed SQL statement: {sql}.')

            # iterate over received data and build returning result

        except sqlite3.Error as error:  # error handler
            log.error(f"Error while working with SQLite:\n{error}")

        finally:  # in any case we have to close the connection to DB
            if cursor:
                cursor.close()
                log.debug("SQLite cursor is closed.")
            if connection:
                connection.close()
                log.debug("SQLite connection is closed.")


    def add_base_ship(self):
        pass

    def get_base_ships(self):
        pass


if __name__ == "__main__":
    # print(MSG_MODULE_ISNT_RUNNABLE)
    config = Config()

    scraper_db = ScraperSQLiteDB(config.db_name, db_schema_init_file=config.db_schema_init_sql,
                                 db_schema_reset_file=config.db_schema_reset_sql)
    # scraper_db.reset_db()
    # scraper_db.init_db()

    start = datetime.now()
    time.sleep(2)
    end = datetime.now()
    params = '--help'

    tele_id = scraper_db.add_scraper_telemetry(start, end, params)
    print('added telemetry:', tele_id)
