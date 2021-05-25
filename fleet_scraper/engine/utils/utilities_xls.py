# coding=utf-8

"""
    Excel-related utilities module for Fleet DB Scraper.

    Useful resources:
        - (excel)       http://www.python-excel.org/
        - (pathlib - 1) https://habr.com/ru/post/453862/
        - (pathlib -2)  https://habr.com/ru/company/otus/blog/540380/ (!)

    Created:  Dmitrii Gusev, 24.05.2021
    Modified:
"""

import xlwt
import logging
from pathlib import Path

# some useful constants
DEFAULT_EXCEL_SHEET_NAME = 'ships'

# todo: implement unit tests for module functions!

# init module logger
log = logging.getLogger('scraper_utilities_xls')


def verify_and_process_file(file_name: str) -> None:
    """Verification of the provided file name and creating all necessary parent dirs in
        the provided file path (if needed).
    :param file_name:
    :return None: ???
    """
    # todo: externalize here excel file checks, perhaps - move it to utilities class?
    pass


def save_base_ships_2_excel(ships: list, xls_file: str) -> None:
    """Save provided list of base ships dto's to xls file. For sheet name default value is used.
    :param ships: ships list to save, if list empty/None - empty excel file will be created
    :param xls_file: excel file to save provided ships, mustn't be empty. Overrides existing file
            by default. If provided path is existing directory - error. If provided long path with
            non-existent directories - all necessary directories will be created.
    :return: None ???
    """
    log.debug(f'save_base_ships_2_excel(): save provided ships map to file: {xls_file}.')

    if not isinstance(ships, list):  # fail-fast -> provided list of ships
        raise ValueError('Not a list provided (ships)!')

    if xls_file is None or len(xls_file.strip()) == 0:  # fail-fast -> check provided xls file name
        raise ValueError('Provided empty excel file name - can\'t save!')

    xls_file_path: Path = Path(xls_file)
    if xls_file_path.is_dir():  # fail-fast -> check if file is existing directory
        raise ValueError(f'Provided file path {xls_file} is an existing directory!')

    xls_file_path.parent.mkdir(parents=True, exist_ok=True)  # create necessary parent dirs in path

    book = xlwt.Workbook()                            # create workbook
    sheet = book.add_sheet(DEFAULT_EXCEL_SHEET_NAME)  # create new sheet

    # create header row
    row = sheet.row(0)
    row.write(0, 'flag')
    row.write(1, 'main_name')
    row.write(2, 'secondary_name')
    row.write(3, 'home_port')
    row.write(4, 'call_sign')
    row.write(5, 'reg_number')
    row.write(6, 'imo_number')

    row_counter = 1
    for ship in ships:  # iterate over ships map with keys / values
        row = sheet.row(row_counter)  # create new row

        row.write(0, ship.flag)
        row.write(1, ship.main_name)
        row.write(2, ship.secondary_name)
        row.write(3, ship.home_port)
        row.write(4, ship.call_sign)
        row.write(5, ship.reg_number)
        row.write(6, ship.imo_number)
        row_counter += 1

    book.save(xls_file)  # save created workbook


def save_extended_ships_2_excel(ships: list, xls_file: str) -> None:
    """???
    :param ships:
    :param xls_file:
    :return None ???
    """
    pass


def load_base_ships_from_excel():
    """"""
    pass


def load_extended_ships_from_excel():
    """"""
    pass


# todo: implement unit tests that module isn't runnable directly!
if __name__ == '__main__':
    print('Don\'t run this utility script directly!')
