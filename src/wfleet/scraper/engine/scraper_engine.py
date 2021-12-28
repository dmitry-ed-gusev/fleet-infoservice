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
from wfleet.scraper.engine.scraper_rsclassorg import RsClassOrgScraper
from wfleet.scraper.engine.scraper_rivregru import RivRegRuScraper
from wfleet.scraper.engine.scraper_morflotru import MorflotRuScraper


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
