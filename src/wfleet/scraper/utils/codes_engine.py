#!/usr/bin/env python3
# coding=utf-8

"""
    Codes processor module for the Fleet Scraper.

    Created:  Gusev Dmitrii, 27.05.2022
    Modified: Gusev Dmitrii, 19.06.2022
"""

import csv
import logging
from pathlib import Path
from typing import Dict, List, Set
from wfleet.scraper.config.scraper_config import Config
from wfleet.scraper.config.scraper_messages import MSG_MODULE_ISNT_RUNNABLE, MSG_NOT_IMPLEMENTED
from wfleet.scraper.exceptions.scraper_exceptions import ScraperException

# init module logger
log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")


class CodesProcessor:
    """CSV-file backed processor for codes list."""

    def __init__(self, file_name: str) -> None:
        log.debug(f'__init__(): initializing CodesListProcessor with file [{file_name}].')
        if not file_name:  # fail-fast for the empty file name
            raise ScraperException("Provided empty file name!")

        if Path(file_name).exists() and not Path(file_name).is_file():
            raise ScraperException(f"Provided file name is not a file: [{file_name}]!")

        # init internal state
        self.__file_name: str = file_name
        self.__codes_list: Set[str] = set()
        self.__load_list()

    def __load_list(self) -> None:
        log.debug(f'__load_list(): loading codes from [{self.__file_name}].')
        codes: Set[str] = set()
        with open(self.__file_name, mode='r') as file:  # read CSV file into internal set
            csv_reader = csv.reader(file, delimiter=';')
            for row in csv_reader:  # process all rows in a file
                codes.add(row[0])
        log.debug(f'Loaded #{len(codes)} codes from [{self.__file_name}].')
        self.__codes_list = sorted(codes)

    def __save_list(self) -> None:
        log.debug(f'__save_list(): saving codes to [{self.__file_name}].')
        with open(self.__file_name, mode='w') as file:  # save codes list to CSV file
            csv_writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for code in sorted(self.__codes_list):  # write codes to CSV file
                csv_writer.writerow([code])
        log.debug(f'Saved #{len(self.__codes_list)} codes to [{self.__file_name}].')

    def codes(self) -> Set[str]:
        log.debug('codes(): returning codes list.')
        return self.__codes_list

    def add(self, code: str) -> None:
        log.debug(f'add(): adding code {code}.')
        # if code not empty and not in the list - add and save list
        if code and code not in self.__codes_list:
            self.__codes_list.add(code)
            self.__save_list()

    def add_all(self, codes: Set[str]) -> None:
        log.debug('add_all(): adding a list of codes.')
        # if codes list is not empty - adding all codes
        if codes:
            self.__codes_list.update(codes)
            self.__save_list()

    def ranges(self, num_of_ranges: int) -> List[Set[str]]:
        log.debug('ranges(): ...')
        # todo: implementation!
        raise NotImplementedError(MSG_NOT_IMPLEMENTED)

    def contains(self, code: str) -> bool:
        if not code:
            return False

        result: bool = code in self.__codes_list
        log.debug(f'contains(): codes list contains code {code} = {result}.')
        return result


class CodesProcessorFactory:
    """Simple hard-coded factory class for the CodesProcessor instances."""

    # todo: remove hardcoded values
    # todo: make methods for getting codes more genric

    # class variables
    processors: Dict[str, CodesProcessor] = dict()
    config: Config = Config()

    @classmethod
    def imo_codes(cls) -> CodesProcessor:
        log.debug('imo_codes(): working.')
        if not cls.processors.get('imo', None):
            log.debug('IMO processor is not initialized yet, initializing.')
            cls.processors['imo'] = CodesProcessor(cls.config.imo_file)
        return cls.processors['imo']

    @classmethod
    def seaweb_shipbuildes_codes(cls):
        log.debug('seaweb_shipbuildes_codes(): working.')
        if not cls.processors.get('seaweb_shipbuilders', None):
            log.debug('Seaweb Shipbuilders processor is not initialized yet, initializing.')
            cls.processors['seaweb_shipbuilders'] = CodesProcessor(cls.config.seaweb_shipbuilders_codes_file)
        return cls.processors['seaweb_shipbuilders']

    @classmethod
    def seaweb_shipcompanies_codes(cls):
        log.debug('seaweb_shipcompanies_codes(): working.')
        if not cls.processors.get('seaweb_shipcompanies', None):
            log.debug('Seaweb Shipcompanies processor is not initialized yet, initializing.')
            cls.processors['seaweb_shipcompanies'] = \
                CodesProcessor(cls.config.seaweb_shipcompanies_codes_file)
        return cls.processors['seaweb_shipcompanies']


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
