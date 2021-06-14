# coding=utf-8

"""
    Excel-related utilities module for Fleet DB Scraper.

    Useful resources:
        - (excel)       http://www.python-excel.org/
        - (pathlib - 1) https://habr.com/ru/post/453862/
        - (pathlib -2)  https://habr.com/ru/company/otus/blog/540380/ (!)

    Created:  Dmitrii Gusev, 24.05.2021
    Modified: Dmitrii Gusev, 13.06.2021
"""

import xlwt
import logging
from pathlib import Path

from typing import List

from . import constants as const
from .utilities import generate_timed_filename
from ..entities.ships import BaseShipDto, ExtendedShipDto

# init module logger
log = logging.getLogger(const.LOGGING_UTILITIES_XLS_LOGGER)


def verify_and_process_xls_file(xls_file: str) -> None:
    """Verification of the provided file name and creating all necessary parent dirs in
        the provided file path (if needed).
    :param xls_file:
    :return None: ???
    """
    if xls_file is None or len(xls_file.strip()) == 0:  # fail-fast -> check provided xls file name
        raise ValueError('Provided empty excel file name!')

    xls_file_path: Path = Path(xls_file)
    if xls_file_path.is_dir():  # fail-fast -> check if file is existing directory
        raise ValueError(f'Provided file path {xls_file} is an existing directory!')

    xls_file_path.parent.mkdir(parents=True, exist_ok=True)  # create necessary parent dirs in path


def save_base_ships_2_excel(ships: List[BaseShipDto], xls_file: str) -> None:
    """Save provided list of base ships dto's to xls file. For sheet name default value is used.
    :param ships: ships list to save, if list empty/None - empty excel file will be created
    :param xls_file: excel file to save provided ships, mustn't be empty. Overrides existing file
            by default. If provided path is existing directory - error. If provided long path with
            non-existent directories - all necessary directories will be created.
    :return: None ???
    """
    log.debug(f'save_base_ships_2_excel(): save provided ships list to xls file: {xls_file}.')

    if not isinstance(ships, list):  # fail-fast -> provided list of ships
        raise ValueError('Not a list provided (ships)!')

    verify_and_process_xls_file(xls_file)  # verify and process xls file

    book = xlwt.Workbook()                            # create workbook
    sheet = book.add_sheet(const.EXCEL_DEFAULT_SHEET_NAME)  # create new sheet

    # create header row
    row = sheet.row(0)
    # ship identity
    row.write(0, 'imo_number')
    row.write(1, 'proprietary_number1')
    row.write(2, 'proprietary_number2')
    row.write(3, 'source_system')
    # ship main value (base data)
    row.write(4, 'flag')
    row.write(5, 'main_name')
    row.write(6, 'secondary_name')
    row.write(7, 'home_port')
    row.write(8, 'call_sign')
    row.write(9, 'extended_url')
    row.write(10, 'datetime')

    row_counter = 1
    for ship in ships:  # iterate over ships map with keys / values
        row = sheet.row(row_counter)  # create new row
        # ship identity
        row.write(0, ship.imo_number)
        row.write(1, ship.proprietary_number1)
        row.write(2, ship.proprietary_number2)
        row.write(3, ship.source_system)
        # ship main value (base data)
        row.write(4, ship.flag)
        row.write(5, ship.main_name)
        row.write(6, ship.secondary_name)
        row.write(7, ship.home_port)
        row.write(8, ship.call_sign)
        row.write(9, ship.extended_info_url)
        # convert datetime to human-readable format
        row.write(10, ship.init_datetime.strftime(const.EXCEL_DEFAULT_TIMESTAMP_PATTERN))

        row_counter += 1

    book.save(xls_file)  # save created workbook


def load_base_ships_from_excel(xls_file: str) -> list:
    """Load ships (BaseShipDto's) form provided excel file.
    :param xls_file:
    :return:
    """
    log.debug(f'load_base_ships_from_excel(): load extended ships from xls file: {xls_file}.')
    verify_and_process_xls_file(xls_file)  # verify and process xls file
    # todo: implementation!
    return list()


def save_extended_ships_2_excel(ships: list, xls_file: str) -> None:
    """Save provided list of extended ships dto's to xls file. For sheet name default value is used.
    :param ships: hips list to save, if list empty/None - empty excel file will be created
    :param xls_file: excel file to save provided ships, mustn't be empty. Overrides existing file
            by default. If provided path is existing directory - error. If provided long path with
            non-existent directories - all necessary directories will be created.
    :return None ???
    """
    log.debug(f'save_extended_ships_2_excel(): save provided ships list to xls file: {xls_file}.')

    if not isinstance(ships, list):  # fail-fast -> provided list of ships
        raise ValueError('Not a list provided (ships)!')

    verify_and_process_xls_file(xls_file)  # verify and process xls file

    book = xlwt.Workbook()  # create workbook
    sheet = book.add_sheet(const.EXCEL_DEFAULT_SHEET_NAME)  # create new sheet

    # create header row
    row_counter = 1
    for ship in ships:  # iterate over ships map with keys / values
        row = sheet.row(row_counter)  # create new row
        # row.write(0, ship.flag) - etc for further values
        row_counter += 1
    # todo: implementation!
    book.save(xls_file)  # save created workbook


def load_extended_ships_from_excel(xls_file: str) -> list:
    """Load ships (ExtendedShipDto's) form provided excel file.
    :param xls_file:
    :return:
    """
    log.debug(f'load_extended_ships_from_excel(): load extended ships from xls file: {xls_file}.')
    verify_and_process_xls_file(xls_file)  # verify and process xls file
    # todo: implementation!
    return list()


def process_scraper_dry_run(system_name: str) -> None:
    log.warning("DRY RUN MODE IS ON!")
    # save empty files to cache with specific postfix
    cache_dir = const.SCRAPER_CACHE_PATH + '/' + generate_timed_filename(system_name +
                                                                         const.SCRAPER_CACHE_DRY_RUN_DIR_SUFFIX)
    save_base_ships_2_excel(list(), cache_dir + '/' + const.EXCEL_BASE_SHIPS_DATA)
    save_extended_ships_2_excel(list(), cache_dir + '/' + const.EXCEL_EXTENDED_SHIPS_DATA)


# todo: implement unit tests that module isn't runnable directly!
if __name__ == '__main__':
    print('Don\'t run this utility script directly!')
