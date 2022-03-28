# coding=utf-8

"""
    Excel-related utilities module for Fleet DB Scraper.

    Useful resources:
        - (excel)       http://www.python-excel.org/
        - (pathlib - 1) https://habr.com/ru/post/453862/
        - (pathlib - 2) https://habr.com/ru/company/otus/blog/540380/ (!)

    Created:  Dmitrii Gusev, 24.05.2021
    Modified: Dmitrii Gusev, 14.12.2021
"""

import xlwt
import logging
from pathlib import Path

from typing import List

from wfleet.scraper.config import scraper_defaults as const
# from .utilities import generate_timed_filename
from wfleet.scraper.entities.ships import ShipDto

# init module logger
# log = logging.getLogger(const.LOGGING_UTILITIES_XLS_LOGGER)
log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")


def verify_and_process_xls_file(xls_file: str) -> None:
    """Verification of the provided file name and creating all necessary parent dirs in
        the provided file path (if needed).
    :param xls_file:
    :return None: ???
    """
    if xls_file is None or len(xls_file.strip()) == 0:  # fail-fast -> check provided xls file name
        raise ValueError("Provided empty excel file name!")

    xls_file_path: Path = Path(xls_file)
    if xls_file_path.is_dir():  # fail-fast -> check if file is existing directory
        raise ValueError(f"Provided file path {xls_file} is an existing directory!")

    xls_file_path.parent.mkdir(parents=True, exist_ok=True)  # create necessary parent dirs in path


def save_ships_2_excel(ships: List[ShipDto], xls_file: str) -> None:
    """Save provided list of ships dto's to xls file. For sheet name default value is used.
    :param ships: ships list to save, if list empty/None - empty excel file will be created
    :param xls_file: excel file to save provided ships, mustn't be empty. Overrides existing file
            by default. If provided path is existing directory - error. If provided long path with
            non-existent directories - all necessary directories will be created.
    :return: None ???
    """
    log.debug(f"save_ships_2_excel(): save provided ships list to xls file: {xls_file}.")

    if not isinstance(ships, list):  # fail-fast -> provided list of ships
        raise ValueError("Not a list provided (ships)!")

    verify_and_process_xls_file(xls_file)  # verify and process xls file

    book = xlwt.Workbook()  # create workbook
    sheet = book.add_sheet(const.EXCEL_DEFAULT_SHEET_NAME)  # create new sheet

    # create header row
    row = sheet.row(0)

    # ship's identity
    row.write(0, "imo_number")
    row.write(1, "proprietary_number1")
    row.write(2, "proprietary_number2")
    row.write(3, "source_system")

    # ship's main value
    row.write(4, "flag")
    row.write(5, "main_name")
    row.write(6, "secondary_name")
    row.write(7, "home_port")
    row.write(8, "call_sign")
    row.write(9, "project")
    row.write(10, "owner")
    row.write(11, "owner_address")
    row.write(12, "owner_ogrn")
    row.write(13, "owner_ogrn_date")

    # ship's additional data
    row.write(14, "build_number")
    row.write(15, "ship_type")
    row.write(16, "build_date")
    row.write(17, "build_place")

    # ship's system info
    # row.write(14, 'extended_url')  # todo: do we need to save it?
    row.write(18, "datetime")

    row_counter = 1
    for ship in ships:  # iterate over ships map with keys / values
        row = sheet.row(row_counter)  # create new row

        # ship's identity
        row.write(0, ship.imo_number)
        row.write(1, ship.proprietary_number1)
        row.write(2, ship.proprietary_number2)
        row.write(3, ship.source_system)

        # ship's main value
        row.write(4, ship.flag)
        row.write(5, ship.main_name)
        row.write(6, ship.secondary_name)
        row.write(7, ship.home_port)
        row.write(8, ship.call_sign)
        row.write(9, ship.project)
        row.write(10, ship.owner)
        row.write(11, ship.owner_address)
        row.write(12, ship.owner_ogrn)
        row.write(13, ship.owner_ogrn_date)

        # ship's additional data
        row.write(14, ship.build_number)
        row.write(15, ship.ship_type)
        row.write(16, ship.build_date)
        row.write(17, ship.build_place)

        # ship's system info
        # row.write(9, ship.extended_info_url)  # todo: do we need to save it?
        # convert datetime to human-readable format
        row.write(18, ship.init_datetime.strftime(const.EXCEL_DEFAULT_TIMESTAMP_PATTERN))

        row_counter += 1

    book.save(xls_file)  # save created workbook


def load_ships_from_excel(xls_file: str) -> List[ShipDto]:
    """Load ships (ShipDto's) form provided excel file.
    :param xls_file:
    :return:
    """
    log.debug(f"load_base_ships_from_excel(): load extended ships from xls file: {xls_file}.")
    verify_and_process_xls_file(xls_file)  # verify and process xls file
    # todo: implementation!
    return list()


# todo: do we need this method?
def save_extended_ships_2_excel(ships: list, xls_file: str) -> None:
    """Save provided list of extended ships dto's to xls file. For sheet name default value is used.
    :param ships: hips list to save, if list empty/None - empty excel file will be created
    :param xls_file: excel file to save provided ships, mustn't be empty. Overrides existing file
            by default. If provided path is existing directory - error. If provided long path with
            non-existent directories - all necessary directories will be created.
    :return None ???
    """
    log.debug(f"save_extended_ships_2_excel(): save provided ships list to xls file: {xls_file}.")

    if not isinstance(ships, list):  # fail-fast -> provided list of ships
        raise ValueError("Not a list provided (ships)!")

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


# todo: do we need this method?
def load_extended_ships_from_excel(xls_file: str) -> list:
    """Load ships (ExtendedShipDto's) form provided excel file.
    :param xls_file:
    :return:
    """
    log.debug(f"load_extended_ships_from_excel(): load extended ships from xls file: {xls_file}.")
    verify_and_process_xls_file(xls_file)  # verify and process xls file
    # todo: implementation!
    return list()


def process_scraper_dry_run(system_name: str) -> None:
    log.warning("DRY RUN MODE IS ON!")
    # save empty files to cache with specific postfix
    cache_dir = (
        const.SCRAPER_CACHE_PATH
        + "/"
        + generate_timed_filename(system_name + const.SCRAPER_CACHE_DRY_RUN_DIR_SUFFIX)
    )
    save_ships_2_excel(list(), cache_dir + "/" + const.EXCEL_SHIPS_DATA)
    # save_extended_ships_2_excel(list(), cache_dir + '/' + const.EXCEL_EXTENDED_SHIPS_DATA)


# todo: implement unit tests that module isn't runnable directly!
if __name__ == "__main__":
    print("Don't run this utility script directly!")
