#!/usr/bin/env python3
# coding=utf-8

"""
    Scraper Engine Module. Manage all scraper operations. Should'n be called
    directly - rather should be imported and functions used.

    Created:  Dmitrii Gusev, 24.12.2021
    Modified:
"""

import os
import logging
import shutil
from wfleet.scraper.config.scraper_config import CONFIG


# init module logging
log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")

def cache_cleanup(dry_run: bool = False) -> list:  # todo: move out
    """Perform cleanup in the scraper raw files cache directory. Returns list of deleted directories.
    :param dry_run: in case of value True - DRY RUN MODE is on and no cleanup will be done.
    :return: list of deleted directories
    """
    log.debug("cache_cleanup(): cleaning up scraper cache (delete dry runs results).")

    deleted_dirs = []  # list of deleted directories

    for filename in os.listdir(const.SCRAPER_CACHE_PATH):
        file_path = os.path.join(const.SCRAPER_CACHE_PATH, filename)
        try:
            if os.path.isdir(file_path) and file_path.endswith(const.SCRAPER_CACHE_DRY_RUN_DIR_SUFFIX):
                log.info(f"Found DRY RUN directory: {file_path} - to be deleted!")
                if dry_run:
                    log.warning("DRY RUN mode is active! No cleanup will be performed!")
                else:
                    shutil.rmtree(file_path)
                deleted_dirs.append(file_path)
            elif os.path.isfile(file_path) or os.path.islink(file_path):
                log.debug(f"Found file/symlink: {file_path}. Skipped.")

        except Exception as e:  # exception with cleanup (deletion of the dir/file/link)
            log.error(f"Failed to delete {file_path}. Reason: {e}")

    return deleted_dirs
