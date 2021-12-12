#!/usr/bin/env python3
# coding=utf-8

"""
    Main Fleet Scraper Module for all particular scrapers.

    Important notes:
      - scraper can be run in 'DRY RUN' mode - nothing will happen, only empty excel files
        will be created in cache (dry run directory will be marked with '-dryrun' postfix.
      - scraper can be run in 'requests number limited mode' - # todo: add description!

    Useful resources:
      - (remove dirs) https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder

    Created:  Gusev Dmitrii, 10.01.2021
    Modified: Dmitrii Gusev, 09.12.2021
"""

# todo: implement cmd line arguments - dry run, requests_limit, threads counter, ???
# todo: create unit tests for dry run mode
# todo: create unit tests for request limited run

# todo: implement multithreading for calling scrapers, some of scrapers will spawn more threads (???)

import os
import shutil
import logging
import logging.config
import wfleet.scraper.config.scraper_defaults as const

# from pyutilities.pylog import setup_logging
# from pyutilities.config import Configuration
from wfleet.scraper.config.scraper_config import CONFIG
from wfleet.scraper.config.logging_config import LOGGING_CONFIG

from wfleet.scraper.engine.scraper_rsclassorg import RsClassOrgScraper
from wfleet.scraper.engine.scraper_rivregru import RivRegRuScraper
from wfleet.scraper.engine.scraper_morflotru import MorflotRuScraper

MAIN_LOGGER: str = "wfleet.scraper"


def scrap_all_data(dry_run: bool = False, requests_limit: int = 0):
    """
    :param dry_run:
    :param requests_limit:
    :return:
    """
    log.debug("scrap_all_data(): processing all data sources.")

    # --- scraper for rivreg.ru
    riv_scraper: RivRegRuScraper = RivRegRuScraper(const.SYSTEM_RIVREGRU, const.SCRAPER_CACHE_PATH)
    riv_scraper.scrap(dry_run=dry_run)
    # --- scraper class for morflot.ru
    morflot_scraper: MorflotRuScraper = MorflotRuScraper(const.SYSTEM_MORFLOTRU, const.SCRAPER_CACHE_PATH)
    morflot_scraper.scrap(dry_run=dry_run)
    # --- scraper for rs-class.org
    rs_scraper: RsClassOrgScraper = RsClassOrgScraper(const.SYSTEM_RSCLASSORG, const.SCRAPER_CACHE_PATH)
    rs_scraper.scrap(dry_run=dry_run, requests_limit=requests_limit)

    # todo: implement the below scrapers properly!
    # # scraper class for gims.ru
    # gims_scraper: GimsRuScraper = GimsRuScraper(const.SYSTEM_GIMS, const.SCRAPER_CACHE_PATH)
    # gims_scraper.scrap(dry_run=dry_run)
    # # scraper class for vesselfinder.com
    # vf_scraper: VesselFinderComScraper = VesselFinderComScraper(const.SYSTEM_VESSELFINDERCOM, const.SCRAPER_CACHE_PATH)
    # vf_scraper.scrap(dry_run=dry_run)
    # # scraper class for clarksons.net
    # clarksons_scraper: ClarksonsNetScraper = ClarksonsNetScraper(const.SYSTEM_CLARKSONSNET, const.SCRAPER_CACHE_PATH)
    # clarksons_scraper.scrap(dry_run=dry_run)
    # # scraper class for marinetraffic.com
    # mtraffic_scraper: MarineTrafficComScraper = MarineTrafficComScraper(const.SYSTEM_MARINETRAFFICCOM,
    #                                                                     const.SCRAPER_CACHE_PATH)
    # mtraffic_scraper.scrap(dry_run=dry_run)


def archive_scraped_data(dry_run: bool = False) -> list:
    """Perform scraper cache archive. returns list of archived directories.
    :param dry_run: in case of value True - DRY RUN MODE is on and no archiving will be done.
    :return: list of archived directories
    """
    log.debug("archive_scraped_data(): processing scraped data and archive processed (saved to db).")
    # todo: implementation!
    return list()


def cache_cleanup(dry_run: bool = False) -> list:
    """Perform cleanup in the scraper cache directory. Returns list of deleted directories.
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


def temp_entry_point():
    """Temporary entry point for console installation."""
    print("Temporary entry point for World Fleet Scraper Utility is working...")


def init_scraper_cache():
    """Initializer for the Scraper cache."""
    print("Initializing World Fleet Scraper cache...")


def init_scraper():
    """Scraper init method."""
    print("Initializing World Fleet Scraper...")


# todo: managing config approach: https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
# todo: https://docs.python.org/3/library/configparser.html

# main part of the script
if __name__ == "__main__":

    # get configuration maps (logging and general)
    config = CONFIG
    logger_config = LOGGING_CONFIG

    # makes sure logging directories exists
    os.makedirs(CONFIG["cache_dir"] + "/logs/", exist_ok=True)

    # init logger with config dictionary
    logging.config.dictConfig(LOGGING_CONFIG)

    # first log message
    log = logging.getLogger(MAIN_LOGGER)
    log.info("Starting World Fleet Scraper.")
    log.debug(f"Logging for module {MAIN_LOGGER} is configured.")
    log.debug(f"Current working dir: {os.getcwd()}")

    init_scraper_cache()  # init cache
    init_scraper()  # init scraper

    # setup_logging(default_path=const.LOGGING_CONFIG_FILE)
    # log.info("Starting Scraper Processor for all source systems...")

    # start all scrapers and get the data
    # scrap_all_data(dry_run=False, requests_limit=0)
    # do cleanup for dry run immediately
    # log.info(f"Cleaned up: {cache_cleanup(False)}")

    # morflot.parse_raw_data('engine/cache/'
    #                        '19-Jun-2021_15-27-34-scraper_morflotru/3926-5792-ts_razdel_3+.xlsx')
