#!/usr/bin/env python3
# coding=utf-8

"""
    Unit tests for utilities class.

    Created:  Dmitrii Gusev, 21.03.2021
    Modified: Dmitrii Gusev, 30.10.2021
"""

# todo: do we need logging in the test class? if yes - review and fix logging!

import unittest
import logging
from wfleet.scraper.utils.utilities import (
    build_variations_hashmap,
    build_variations_list,
    get_hash_bucket_number,
    add_value_to_hashmap,
)
from pyutilities.pylog import setup_logging

# some useful constants
LOGGER_NAME = "scraper_rsclassorg_test"


class TestUtilities(unittest.TestCase):

    # static logger initializer
    setup_logging(default_path="../../test_logging.yml")
    # log = logging.getLogger(LOGGER_NAME)

    def setUp(self):
        self.log = logging.getLogger(LOGGER_NAME)
        self.log.debug("TestUtilities.setUp()")

    def tearDown(self):
        self.log.debug("TestUtilities.tearDown()")

    @classmethod
    def setUpClass(cls):
        cls.log = logging.getLogger(LOGGER_NAME)
        cls.log.debug("TestUtilities.setUpClass()")

    @classmethod
    def tearDownClass(cls):
        cls.log.debug("TestUtilities.tearDownClass()")

    def test_get_hash_bucket_number_empty_value(self):
        self.assertRaises(ValueError, lambda: get_hash_bucket_number(None, 2))
        self.assertRaises(ValueError, lambda: get_hash_bucket_number("", 2))
        self.assertRaises(ValueError, lambda: get_hash_bucket_number("   ", 2))

    def test_get_hash_bucket_number_0_or_less_buckets(self):
        self.assertEqual(0, get_hash_bucket_number("aaa", 0))
        self.assertEqual(0, get_hash_bucket_number("bbb", -1))
        self.assertEqual(0, get_hash_bucket_number("ccc", -19))

    def test_get_hash_bucket_number(self):
        self.assertEqual(9, get_hash_bucket_number("ccc", 10))
        self.assertEqual(4, get_hash_bucket_number("ccc", 5))

    def test_add_value_to_hashmap_empty_or_none_hashmap(self):
        self.assertRaises(ValueError, lambda: add_value_to_hashmap(None, "aaa", 0))
        self.assertRaises(ValueError, lambda: add_value_to_hashmap(list(), "aaa", 0))

    def test_add_value_to_hashmap_empty_or_none_value(self):
        self.assertRaises(ValueError, lambda: add_value_to_hashmap(dict(), "", 0))
        self.assertRaises(ValueError, lambda: add_value_to_hashmap(dict(), "   ", 0))
        self.assertRaises(ValueError, lambda: add_value_to_hashmap(dict(), None, 0))

    def test_add_value_to_hashmap(self):
        self.assertEqual({0: ["aaa"]}, add_value_to_hashmap(dict(), "aaa", 0))
        self.assertEqual({0: ["aaa", "bbb"]}, add_value_to_hashmap({0: ["aaa"]}, "bbb", 0))
        self.assertEqual(
            {0: ["aaa", "bbb"], 4: ["ccc"]},
            add_value_to_hashmap({0: ["aaa", "bbb"]}, "ccc", 5),
        )

    # def test_build_variations_hashmap_0_buckets(self):
    #     self.assertEqual(1, len(build_variations_hashmap().keys()))

    # def test_build_variations_hashmap(self):
    #     self.assertEqual(10, len(build_variations_hashmap(10).keys()))

    # def test_build_variations_list(self):
    #     self.assertTrue(isinstance(build_variations_list(), list))
    #     self.assertEqual(9522, len(build_variations_list()))

    # def test_generate_timed_filename(self):
    #     self.assertTrue(generate_timed_filename("     postfix  ").endswith("-postfix"))


if __name__ == "__main__":
    unittest.main()
