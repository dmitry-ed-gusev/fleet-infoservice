#!/usr/bin/env python3
# coding=utf-8

"""
    World Fleet Scraper configuration for the application. In case cache dir [.wfleet] exists
    in the current dir - use it, otherwise cache dir will be placed/used in the use home dir.

    Useful materials:
      - https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
      - https://python.plainenglish.io/singleton-class-in-java-vs-python-554bbcee3470
      - https://elbenshira.com/blog/singleton-pattern-in-python/

    Created:  Gusev Dmitrii, 12.12.2021
    Modified: Dmitrii Gusev, 27.05.2022
"""

import os
import json
from pathlib import Path
from dataclasses import asdict
from dataclasses import dataclass
from wfleet.scraper.utils.utilities import singleton

# common system messages
MSG_MODULE_ISNT_RUNNABLE = "This module is not runnable!"
MSG_NOT_IMPLEMENTED: str = "Not implemented yet!"
# common constants/defaults
CACHE_DIR_NAME: str = ".wfleet"  # cache dir name


# if cache is in curr dir (exists and is dir) - use it, otherwise - use the user
# home directory (mostly suitable for development, in most cases user home dir will be used)
def get_cache_dir(base_name: str) -> str:
    if not base_name:
        raise ValueError("Empty base name!")

    if Path(base_name).exists() and Path(base_name).is_dir():
        return base_name
    else:  # cache dir not exists or is not a dir
        return str(Path.home()) + '/' + base_name


@singleton
@dataclass(frozen=True)
class Config():
    # -- basic directories settings
    cache_dir: str = get_cache_dir(CACHE_DIR_NAME)
    log_dir: str = cache_dir + "/logs"  # log directory
    work_dir: str = str(os.getcwd())  # current working dir
    user_dir: str = str(Path.home())  # user directory
    cache_raw_files_dir: str = cache_dir + "/.scraper_raw_files"  # raw files dir in the cache

    # -- some useful defaults
    app_name: str = "World Fleet Scraper"
    encoding: str = "utf-8"  # general encoding
    timestamp_pattern: str = "%d-%b-%Y %H:%M:%S"  # general timestamp for the app
    default_requests_limit: int = 100000  # default limit for HTTP requests
    default_timeout_delay_max: int = 4  # max timeout between HTTP requests, seconds
    default_timeout_cadence: int = 100  # timeout cadence - # of HTTP requests between timeout/delay

    # -- IMO numbers management settings
    imo_file: str = cache_dir + "/imo_numbers.csv"  # file with IMO numbers
    imo_file_backup: str = cache_dir + "/imo_numbers.bak"  # file with IMO - backup

    # -- scraper DB settings (SQLite - ?)
    db_dir: str = cache_dir + "/.scraper_db"  # DB dir + DB name (SQLite)
    db_name: str = ".scraperdb"  # DB name (sqlite?)

    # -- some default files names
    raw_data_file: str = "ships_data.xls"
    main_ship_data_file: str = "ship_main.html"

    # -- seaweb scraper/parser settings
    seaweb_base_dir: str = cache_dir + "/.seaweb_db"
    seaweb_raw_ships_dir: str = seaweb_base_dir + "/seaweb"
    seaweb_raw_builders_dir: str = seaweb_base_dir + "/shipbuilders"
    seaweb_raw_companies_dir: str = seaweb_base_dir + "/shipcompanies"
    seaweb_shipbuilders_codes_file: str = seaweb_raw_builders_dir + '/shipbuilders.csv'
    seaweb_shipcompanies_codes_file: str = seaweb_raw_companies_dir + '/shipcompanies.csv'

    def __post_init__(self):  # post-init method - create necessary sub-dirs
        os.makedirs(str(self.log_dir), exist_ok=True)

    def __repr__(self):
        return "Config " + json.dumps(asdict(self), indent=4)


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
