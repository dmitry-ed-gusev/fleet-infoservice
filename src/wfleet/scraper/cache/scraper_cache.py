#!/usr/bin/env python3
# coding=utf-8

"""
    Scraper Cache Module. Manages Scraper's local cache (storage for raw data files from sources)
    This module should'n be called directly - rather be imported and functions used.

    Created:  Dmitrii Gusev, 01.01.2022
    Modified: Dmitrii Gusev, 30.03.2022
"""

import os
import re
import shutil
import logging
from datetime import datetime
from typing import Pattern
from pathlib import Path
from wfleet.scraper.exceptions.scraper_exceptions import ScraperException
from wfleet.scraper.config.scraper_config import CONFIG, MSG_MODULE_ISNT_RUNNABLE

# todo: create cache class in order to merge cache properties and cache operations..?

# timestamp pattern for cache dir
DIR_TIMESTAMP_PATTERN: str = "%Y-%m-%d_%H-%M-%S"  # example: 2021-02-01_22:01:20
# regex: exact start of the string -> sample: YYYY-MM-DD_HH-mm-SS-...
DIR_TIMESTAMP_REGEX: Pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}-)')
# in case of dry run mode - this suffix will be added to the directory
DIR_SUFFIX_DRY_RUN: str = "-dryrun"
# in case of "requests limited" mode - this suffix will be added to the directory
DIR_SUFFIX_LIMITED_REQUESTS_RUN = "-requests-limited"
# exception list used by cache cleanup functions
CACHE_EXCEPTION_LIST: list = ["readme.txt"]

# init module logging
log = logging.getLogger(__name__)
# log.debug(f"Logging for module {__name__} is configured.")


def _cache_find_invalid_entries() -> list:
    """Perform cleanup in the scraper raw files cache directory. Returns list of deleted directories.
    In case of dry run mode - returns list of directories for removal.
    :return: list of items (dirs/files) intended for deletion
    """
    log.debug("cache_find_invalid_entries(): search for invalid entries in scraper cache.")

    invalid_items = []  # list of invalid items in cache folder
    cache_dir: str = CONFIG['cache_raw_files_dir']

    for item in os.listdir(cache_dir):
        match_object = DIR_TIMESTAMP_REGEX.search(item)
        full_path: Path = Path(cache_dir + '/' + item)  # absolute (full) path

        # find any "garbage" - no dirs and dirs with wrong names
        if not full_path.is_dir() or not match_object or item.endswith(DIR_SUFFIX_DRY_RUN):

            if item in CACHE_EXCEPTION_LIST:  # skip item from exception list
                log.debug(f"Item [{item}] is in exceptions list - skipped.")
                continue

            log.debug(f"Found invalid entry [{item}] -> is dir = {full_path.is_dir()}")
            invalid_items.append(str(full_path))  # add entry to the invalid items list

    return invalid_items


def _cache_remove_invalid_entries(invalid_items: list, dry_run: bool) -> None:
    """Physically remove invalid entries in the cache directory. Internal method - shouldn't be used
    separately.
    :invalid_items: list of items for deletion
    :param dry_run: in case of value True - DRY RUN MODE is on and no cleanup will be done.
    :return: null
    """
    log.debug("_cache_remove_invalid_entries(): cleaning up scraper cache.")
    log.debug(f"Got the following entries list:\n{invalid_items}")

    if not invalid_items or len(invalid_items) == 0:  # empty provided list - return
        log.warning("Provided invalid items list is empty!")
        return

    if dry_run:  # dry run mode is on
        log.warning("Dry run mode is on! No deletion...")
        return

    for item in invalid_items:
        try:
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
        except Exception as e:
            log.error(f"Failed to delete {item}. Reason: {e}")


def cache_cleanup(dry_run: bool) -> None:
    """Perform cache cleanup - just a link mthod calling internal implementation methods.
    :param dry_run: dry run - true/false
    """
    log.debug("cache_cleanup(): perform cache cleanup.")
    invalid_items: list = _cache_find_invalid_entries()
    _cache_remove_invalid_entries(invalid_items, dry_run)


def _cache_generate_raw_dir_name(timestamp: datetime, name: str, dry_run: bool, requests_number: int) -> str:
    """Generate cache dir name with provided timestamp and name. If dry run parameter is true - add
    appropriate postfix to the name. If requests limited mode is on - add the suffix as well. The only 
    one suffix will be added, dry run mode suffix overrides the requests limited mode suffix.
    :param timestamp: timestamp for the dir
    :param name: general dir name
    :param dry_run: dry run mode - true/false
    :param requests_limit: requests limited mode if this parameter is > 0
    :return: created dir name (in the cache directory)
    """
    log.debug("cache_create_cache_dir(): creating new cache directory.")

    if not name:  # fail-fast, in case of empty dir name
        raise ScraperException("Provided empty cache directory name!")

    # generate the base name - without any suffixes
    result: str = timestamp.strftime(DIR_TIMESTAMP_PATTERN) + '_' + name

    if dry_run:  # dry-run mode is on
        result += DIR_SUFFIX_DRY_RUN
    elif requests_number > 0:  # requests limited mode is on
        result += DIR_SUFFIX_LIMITED_REQUESTS_RUN

    return result


def cache_get_raw_dir() -> str:
    
    # todo: build raw dir path and create it (if exists and is a dir - OK) and return it
    
    pass


def cache_get_raw_file(file_name: str) -> str:
    
    # todo: us cache_get_raw_dir() function...
    
    pass


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
