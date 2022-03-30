#!/usr/bin/env python3
# coding=utf-8

"""
    World Fleet Scraper configuration for the application. In case cache dir [.wfleet] exists
    in the current dir - use it, otherwise cache dir will be placed/used in the use home dir.

    Useful materials:
      - https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b

    Created:  Gusev Dmitrii, 12.12.2021
    Modified: Dmitrii Gusev, 30.03.2022
"""

import os
from pathlib import Path

CACHE_DIR_NAME: str = ".wfleet"  # cache dir name
MSG_MODULE_ISNT_RUNNABLE = "This module is not runnable!"

# if cache is in curr dir (exists and is dir) - use it, otherwise - use the user
# home directory (mostly suitable for development, in most cases user home dir will be used)
cache_dir: str = ""
if Path(CACHE_DIR_NAME).exists() and Path(CACHE_DIR_NAME).is_dir():
    cache_dir = CACHE_DIR_NAME
else:  # cache dir not exists or is not a dir
    cache_dir = str(Path.home()) + '/' + CACHE_DIR_NAME

# configuration dictionary
CONFIG = {
    "encoding": "utf-8",
    "work_dir": os.getcwd(),
    "cache_dir": cache_dir,  # absolute path to cache
    "cache_raw_files_dir": cache_dir + "/.scraper_raw_files",  # raw files dir in the cache
    "cache_logs_dir": cache_dir + "/logs",  # logs dir
    "db_dir": cache_dir + "/.scraper_db",  # DB dir
    "db_name": ".scraperdb",  # DB name (sqlite?)
    "raw_data_file": "ships_data.xls"
}

# makes sure logging directories exists
os.makedirs(CONFIG["cache_logs_dir"], exist_ok=True)


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
