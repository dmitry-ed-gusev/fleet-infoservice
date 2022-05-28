# coding=utf-8

"""
    Codes processor module for the Fleet Scraper.

    Created:  Gusev Dmitrii, 27.05.2022
    Modified:
"""

import csv
import logging
from pathlib import Path
from typing import List, Set
from wfleet.scraper.config.scraper_config import Config
from wfleet.scraper.utils.utilities import singleton
from wfleet.scraper.config.scraper_config import MSG_MODULE_ISNT_RUNNABLE, MSG_NOT_IMPLEMENTED
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
        self.__codes_list = codes

    def __save_list(self) -> None:
        log.debug(f'__save_list(): saving codes to [{self.__file_name}].')
        with open(self.__file_name, mode='w') as file:  # save codes list to CSV file
            csv_writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for code in sorted(self.__codes_list):  # write codes to CSV file
                csv_writer.writerow([code])
        log.debug(f'Saved #{len(self.__codes_list)} codes to [{self.__file_name}].')

    def get_codes(self) -> Set[str]:
        log.debug('get_list(): returning codes list.')
        return self.__codes_list

    def add(self, code: str) -> None:
        log.debug(f'add_code(): adding code {code}.')
        # if code not empty and not in the list - add and save list
        if code and code not in self.__codes_list:
            self.__codes_list.add(code)
            self.__save_list()

    def get_ranges(self, num_of_ranges: int) -> List[Set[str]]:
        log.debug('get_ranges(): ...')
        # todo: implementation!
        raise NotImplementedError(MSG_NOT_IMPLEMENTED)

    def contains(self, code: str) -> bool:
        log.debug('contains(): ...')
        # todo: implementation!
        raise NotImplementedError(MSG_NOT_IMPLEMENTED)


@singleton
class CodesProcessorFactory:
    """Simple hard-coded factory class for the CodesProcessor instances."""

    processors = dict()

    @cls
    def get_imo_numbers():
        pass


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
