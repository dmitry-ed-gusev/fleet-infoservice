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
      - (click library) https://click.palletsprojects.com/en/8.0.x/

    Created:  Gusev Dmitrii, 10.01.2021
    Modified: Dmitrii Gusev, 20.12.2021
"""

# todo: create unit tests for dry run mode
# todo: create unit tests for request limited run
# todo: implement multithreading for calling scrapers, some of scrapers will spawn more threads (???)

import os
import shutil
import logging
import logging.config
import click
import wfleet.scraper.config.scraper_defaults as const

from wfleet.scraper.config.scraper_config import CONFIG
from wfleet.scraper.config.logging_config import LOGGING_CONFIG
from wfleet.scraper.engine.scraper_rsclassorg import RsClassOrgScraper
from wfleet.scraper.engine.scraper_rivregru import RivRegRuScraper
from wfleet.scraper.engine.scraper_morflotru import MorflotRuScraper

# -- main scraper logger, application name
MAIN_LOGGER: str = "wfleet.scraper"
APP_NAME: str = "World Fleet Scraper"

log = logging.getLogger(MAIN_LOGGER)  # main module logger


def scrap_all_data(dry_run: bool = False, requests_limit: int = 0):  # todo: move out
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


@click.group()
@click.option('--dry-run', default=False, is_flag=True, help='Dry run for scraper (if present).')
def scraper_main(dry_run: bool):
    """World Fleet Scraper. (C) Dmitrii Gusev, Sergei Lukin, 2020-2022."""

    # print(CONFIG)  # just a debug output
    
    # makes sure logging directories exists
    os.makedirs(CONFIG["cache_dir"] + "/logs/", exist_ok=True)
    # init logger with config dictionary
    logging.config.dictConfig(LOGGING_CONFIG)

    # log some initial info
    log.info(f"{APP_NAME} application init finished OK. Starting the application.")
    log.debug(f"Logging for module {MAIN_LOGGER} is configured.")
    log.debug(f"Working dir: {os.getcwd()}")
    log.debug(f"Scraper cache dir: {CONFIG['cache_dir']}")

    if dry_run:  # dry run mode on - warning
        log.warning(f"DRY RUN MODE IS ON!")

    # run cache cleanup
    # run scraper itself


@scraper_main.command()
def cleanup():
    print("cleanup")


@scraper_main.command()
def scrap():
    print("scrap")
    
    
if __name__ == '__main__':
    scraper_main()
