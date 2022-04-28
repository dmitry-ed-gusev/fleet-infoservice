#!/usr/bin/env python3
# coding=utf-8

"""
    Defaults for the Seweb database Scraper/Parser.

    Created:  Gusev Dmitrii, 17.04.2022
    Modified: Dmitrii Gusev, 28.04.2022
"""

import os

# some useful constants
LIMIT = 100000  # requests limit
TIMEOUT_DELAY_MAX = 4  # max timeout between requests, seconds
TIMEOUT_CADENCE = 100  # timeout cadence - # of requests between timeout/delay
IMO_NUMBERS_FILE = "EquasisToIACS_20220401_731.csv"  # csv file with imo numbers (warning - format!)
# base scraper/parser working dir
BASE_WORKING_DIR = os.getcwd() + "/.wfleet/.seaweb_db"
# various working dirs - for ships/builders/companies
RAW_SHIPS_DIR = BASE_WORKING_DIR + "/seaweb"
RAW_BUILDERS_DIR = BASE_WORKING_DIR + "/shipbuilders"
RAW_COMPANIES_DIR = BASE_WORKING_DIR + "/shipcompanies"
# main ship data file name
MAIN_SHIP_DATA_FILE = "ship_main.html"
