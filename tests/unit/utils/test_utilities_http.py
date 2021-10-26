#!/usr/bin/env python3
# coding=utf-8

"""
    Unit tests for http-related utilities class.

    Created:  Dmitrii Gusev, 02.06.2021
    Modified:
"""

# todo: do we need logging in the test class? if yes - review and fix logging!

import unittest
import logging
import responses

from fleet_scraper.engine.utils.utilities_http import perform_file_download_over_http
from pyutilities.pylog import setup_logging

# some useful constants
LOGGER_NAME = 'scraper_rsclassorg_test'


class TestUtilitiesHttp(unittest.TestCase):

    # static logger initializer
    setup_logging(default_path='../../test_logging.yml')

    def setUp(self):
        self.log = logging.getLogger(LOGGER_NAME)
        self.log.debug("TestUtilitiesHttp.setUp()")

    def tearDown(self):
        self.log.debug("TestUtilitiesHttp.tearDown()")

    @classmethod
    def setUpClass(cls):
        cls.log = logging.getLogger(LOGGER_NAME)
        cls.log.debug("TestUtilitiesHttp.setUpClass()")

    @classmethod
    def tearDownClass(cls):
        cls.log.debug("TestUtilitiesHttp.tearDownClass()")

    def test_perform_file_download_over_http_empty_url(self):
        self.assertRaises(ValueError, lambda: perform_file_download_over_http(None, 'dir'))
        self.assertRaises(ValueError, lambda: perform_file_download_over_http('', 'dir'))
        self.assertRaises(ValueError, lambda: perform_file_download_over_http('    ', 'dir'))

    # todo: fix the test
    # @responses.activate
    # def test_downloads_file(self):
    #     url = 'http://example.org/excel.xls'
    #     with open('./utils_test_files/excel.xls', 'rb') as excel_file:
    #         responses.add(responses.GET, url,
    #                       body=excel_file.read(), status=200,
    #                       content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    #                       adding_headers={'Transfer-Encoding': 'chunked'})
    #         filename = perform_file_download_over_http(url, './zzz/aaa')
    #         # assert things here.


if __name__ == '__main__':
    unittest.main()
