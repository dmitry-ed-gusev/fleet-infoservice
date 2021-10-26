#!/usr/bin/env python3
# coding=utf-8

"""
    Test for excel-related utilities class.

    Created:  Dmitrii Gusev, 24.05.2021
    Modified: Dmitrii Gusev, 30.05.2021
"""

import unittest
import logging
from pathlib import Path
from pyutilities.pylog import setup_logging
from fleet_scraper.engine.entities.ships import ShipDto #, ExtendedShipDto
from fleet_scraper.engine.utils.utilities_xls import save_ships_2_excel, save_extended_ships_2_excel, \
     load_ships_from_excel, load_extended_ships_from_excel

# some useful constants
LOGGER_NAME = 'scraper_rsclassorg_test'
LOGGER_CONFIG_FILE = '../../test_logging.yml'

DIRECTORY_NAME_EMPTY = 'empty_dir'
EXCEL_FILE_NAME_EMPTY = 'empty_excel_file_name.xls'
EXCEL_FILE_NAME_SAVE = 'excel_file_for_save.xls'
EXCEL_FILE_NAME_LOAD = 'excel_file_for_load.xls'


class TestUtilitiesXls(unittest.TestCase):

    # static logger initializer
    setup_logging(default_path=LOGGER_CONFIG_FILE)
    # log = logging.getLogger(LOGGER_NAME)

    def setUp(self):
        self.log = logging.getLogger(LOGGER_NAME)
        self.log.debug("TestUtilitiesXls.setUp()")

    def tearDown(self):
        self.log.debug("TestUtilitiesXls.tearDown()")

    @classmethod
    def setUpClass(cls):
        cls.log = logging.getLogger(LOGGER_NAME)
        cls.log.debug("TestUtilitiesXls.setUpClass()")

    @classmethod
    def tearDownClass(cls):
        cls.log.debug("TestUtilitiesXls.tearDownClass()")
        # remove unnecessary excel files after all test in a class
        xls: Path = Path(EXCEL_FILE_NAME_EMPTY)
        xls.unlink(missing_ok=True)
        xls: Path = Path(EXCEL_FILE_NAME_SAVE)
        xls.unlink(missing_ok=True)

    def test_verify_and_process_xls_file(self):
        # todo: implementation!
        pass

    def test_save_base_ships_2_excel_empty_xls_file_name(self):
        self.assertRaises(ValueError, lambda: save_ships_2_excel(list(), None))
        self.assertRaises(ValueError, lambda: save_ships_2_excel(list(), ''))
        self.assertRaises(ValueError, lambda: save_ships_2_excel(list(), '     '))

    def test_save_base_ships_2_excel_xls_file_is_a_directory(self):
        # create empty dir in the current folder
        empty_dir: Path = Path(DIRECTORY_NAME_EMPTY)
        empty_dir.mkdir()
        # test / assert
        self.assertRaises(ValueError, lambda: save_ships_2_excel(list(), DIRECTORY_NAME_EMPTY))
        # cleanup - remove created dir
        empty_dir.rmdir()

    def test_save_base_ships_2_excel_empty_ships_list(self):
        save_ships_2_excel(list(), EXCEL_FILE_NAME_EMPTY)
        empty_file: Path = Path(EXCEL_FILE_NAME_EMPTY)
        self.assertTrue(empty_file.exists())  # todo: add more checks / content checks
        self.assertTrue(empty_file.is_file())

    def test_save_base_ships_2_excel(self):
        ship1: ShipDto = ShipDto('123456', '987654', "", 'system1')
        ship1.flag = 'flag1'
        ship1.main_name = 'name1'
        ship1.secondary_name = 'secondary1'
        ship1.home_port = 'port1'
        ship1.call_sign = 'sign1'
        ship1.extended_info_url = 'URL1'

        ship2: ShipDto = ShipDto('1234567', '9876543', "", 'system2')
        ship2.flag = 'flag2'
        ship2.main_name = 'name2'
        ship2.secondary_name = 'secondary2'
        ship2.home_port = 'port2'
        ship2.call_sign = 'sign2'
        ship2.extended_info_url = 'URL2'

        ships: list = [ship1, ship2]
        save_ships_2_excel(ships, EXCEL_FILE_NAME_SAVE)

        xls_file: Path = Path(EXCEL_FILE_NAME_SAVE)
        self.assertTrue(xls_file.exists())  # todo: add more checks / content checks
        self.assertTrue(xls_file.is_file())


    # def test_save_extended_ships_2_excel_empty_ships(self):
    #     pass
    #
    # def test_save_extended_ships_2_excel(self):
    #     pass
    #
    # def test_load_base_ships_from_excel(self):
    #     pass
    #
    # def test_load_extended_ships_from_excel(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
