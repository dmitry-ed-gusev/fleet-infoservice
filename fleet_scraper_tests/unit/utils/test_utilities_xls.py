#!/usr/bin/env python3
# coding=utf-8

"""
    Test for excel-related utilities class.

    Created:  Dmitrii Gusev, 24.05.2021
    Modified:
"""

import unittest
import logging
from pathlib import Path
from pyutilities.pylog import setup_logging
from fleet_scraper.engine.entities.ships import BaseShipDto, ExtendedShipDto
from fleet_scraper.engine.utils.utilities_xls import save_base_ships_2_excel, save_extended_ships_2_excel
from fleet_scraper.engine.utils.utilities_xls import load_base_ships_from_excel, load_extended_ships_from_excel

# some useful constants
LOGGER_NAME = 'scraper_rsclassorg_test'
LOGGER_CONFIG_FILE = '../../test_logging.yml'
EMPTY_EXCEL_FILE_NAME = 'empty_excel_file_name.xls'
EMPTY_DIRECTORY_NAME = 'empty_dir'


class TestUtilitiesXls(unittest.TestCase):

    # static logger initializer
    setup_logging(default_path=LOGGER_CONFIG_FILE)
    # log = logging.getLogger(LOGGER_NAME)

    def setUp(self):
        self.log = logging.getLogger(LOGGER_NAME)
        self.log.debug("TestUtilitiesXls.setUp()")

    def tearDown(self):
        self.log.debug("TestUtilitiesXls.tearDown()")
        # remove empty excel file after all test in a class
        empty_xls: Path = Path(EMPTY_EXCEL_FILE_NAME)
        empty_xls.unlink(missing_ok=True)

    @classmethod
    def setUpClass(cls):
        cls.log = logging.getLogger(LOGGER_NAME)
        cls.log.debug("TestUtilitiesXls.setUpClass()")

    @classmethod
    def tearDownClass(cls):
        cls.log.debug("TestUtilitiesXls.tearDownClass()")

    def test_save_base_ships_2_excel_empty_xls_file_name(self):
        self.assertRaises(ValueError, lambda: save_base_ships_2_excel(list(), None))
        self.assertRaises(ValueError, lambda: save_base_ships_2_excel(list(), ''))
        self.assertRaises(ValueError, lambda: save_base_ships_2_excel(list(), '     '))

    def test_save_base_ships_2_excel_xls_file_is_a_directory(self):
        # create empty dir in the current folder
        empty_dir: Path = Path(EMPTY_DIRECTORY_NAME)
        empty_dir.mkdir()
        # test / assert
        self.assertRaises(ValueError, lambda: save_base_ships_2_excel(list(), EMPTY_DIRECTORY_NAME))
        # cleanup - remove created dir
        empty_dir.rmdir()

    def test_save_base_ships_2_excel_empty_ships_list(self):
        save_base_ships_2_excel(list(), EMPTY_EXCEL_FILE_NAME)
        empty_file: Path = Path(EMPTY_EXCEL_FILE_NAME)
        self.assertTrue(empty_file.exists())

    def test_save_base_ships_2_excel(self):
        ship1: BaseShipDto = BaseShipDto('123456')
        ship1.reg_number = '123456'
        ship1.flag = 'flag1'
        ship1.main_name = 'name1'
        ship1.secondary_name = 'secondary1'
        ship1.home_port = 'port1'
        ship1.call_sign = 'sign1'

        ship2: BaseShipDto = BaseShipDto('1234567')
        ship2.reg_number = '1234567'
        ship2.flag = 'flag2'
        ship2.main_name = 'name2'
        ship2.secondary_name = 'secondary2'
        ship2.home_port = 'port2'
        ship2.call_sign = 'sign2'
        # todo: create list with two members
        # todo: save to excel
        # todo: check created excel

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
