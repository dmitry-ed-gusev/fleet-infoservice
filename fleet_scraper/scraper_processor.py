#!/usr/bin/env python3
# coding=utf-8

"""
    Main Fleet Scraper Module for all particular scrapers.

    Important notes:
      - scraper can be run in 'DRY RUN' mode - nothing will happen, only empty excel files
        will be created in cache (dry run directory will be marked with '-dryrun' postfix.
      - ???

    Created:  Gusev Dmitrii, 10.01.2021
    Modified: Dmitrii Gusev, 29.05.2021
"""

# todo: finish implementation
# todo: extract common scraper functions into utilities module
# todo: implement cmd line arguments - dry run, maybe others...

import logging
from pyutilities.pylog import setup_logging

import engine.utils.constants as const
from engine.scraper_rsclassorg import RsClassOrgScraper
from engine.scraper_rivregru import RivRegRuScraper
from engine.scraper_morflotru import MorflotRuScraper
from engine.scraper_gims import GimsRuScraper
from engine.scraper_vesselfindercom import VesselFinderComScraper
from engine.scraper_clarksonsnet import ClarksonsNetScraper
from engine.scraper_marinetrafficcom import MarineTrafficComScraper

# setup logging for the whole script
log = logging.getLogger(const.LOGGING_SCRAPER_PROCESSOR_LOGGER)


def scrap_all_data(dry_run: bool = True):
    """
    :param dry_run:
    :return:
    """
    log.debug("scrap_all_data(): processing all data sources.")

    # scraper class for rs-class.org
    rs_scraper: RsClassOrgScraper = RsClassOrgScraper(const.SYSTEM_RSCLASSORG, const.SCRAPER_CACHE_PATH)
    rs_scraper.scrap(dry_run=True)

    # scraper class for rivreg.ru
    riv_scraper: RivRegRuScraper = RivRegRuScraper(const.SYSTEM_RIVREGRU, const.SCRAPER_CACHE_PATH)
    riv_scraper.scrap(dry_run=True)

    # scraper class for morflot.ru
    morflot_scraper: MorflotRuScraper = MorflotRuScraper(const.SYSTEM_MORFLOTRU, const.SCRAPER_CACHE_PATH)
    morflot_scraper.scrap(dry_run=True)

    # scraper class for gims.ru
    gims_scraper: GimsRuScraper = GimsRuScraper(const.SYSTEM_GIMS, const.SCRAPER_CACHE_PATH)
    gims_scraper.scrap(dry_run=True)

    # scraper class for vesselfinder.com
    vf_scraper: VesselFinderComScraper = VesselFinderComScraper(const.SYSTEM_VESSELFINDERCOM, const.SCRAPER_CACHE_PATH)
    vf_scraper.scrap(dry_run=True)

    # scraper class for clarksons.net
    clarksons_scraper: ClarksonsNetScraper = ClarksonsNetScraper(const.SYSTEM_CLARKSONSNET, const.SCRAPER_CACHE_PATH)
    clarksons_scraper.scrap(dry_run=True)

    # scraper class for marinetraffic.com
    mtraffic_scraper: MarineTrafficComScraper = MarineTrafficComScraper(const.SYSTEM_MARINETRAFFICCOM, const.SCRAPER_CACHE_PATH)
    mtraffic_scraper.scrap(dry_run=True)


# main part of the script
if __name__ == '__main__':
    setup_logging(default_path=const.LOGGING_CONFIG_FILE)
    log.info("Starting Scraper Processor for all sources...")

    # start all scrapers
    scrap_all_data()
