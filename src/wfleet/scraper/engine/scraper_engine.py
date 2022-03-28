#!/usr/bin/env python3
# coding=utf-8

"""
    Scraper Engine Module. Manage all scraper operations. Should'n be called
    directly - rather should be imported and functions used.

    Created:  Dmitrii Gusev, 24.12.2021
    Modified: Dmitrii Gusev, 28.03.2022
"""

import logging
from datetime import datetime
from wfleet.scraper.config.scraper_config import CONFIG

from wfleet.scraper.engine.scrapers.scraper_clarksonsnet import ClarksonsNetScraper
from wfleet.scraper.engine.scrapers.scraper_gims import GimsRuScraper
from wfleet.scraper.engine.scrapers.scraper_rivregru import RivRegRuScraper
from wfleet.scraper.engine.scrapers.scraper_morflotru import MorflotRuScraper

# init module logging
log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")


# todo: implement - one timestamp for all scrapers
# todo: add DB support for scraper runs telemetry
# todo: add execution time measurement for particular scrapers
def scrap_all_data(dry_run: bool = False, requests_limit: int = 0):
    """Perform data scraping with all scrapers/parsers.
    :param dry_run: dry run mode true/false.
    :param requests_limit: limit http/https requests # for some parsers.
    """
    log.debug("scrap_all_data(): processing all data sources.")

    # scraper run timestamp
    timestamp: datetime = datetime.now()

    # --- run scraper for clarcksons.net
    clarksons_scraper: ClarksonsNetScraper = ClarksonsNetScraper()
    clarksons_scraper.scrap(timestamp, dry_run=dry_run, requests_limit=requests_limit)

    # --- run scraper class for GIMS
    gims_scraper: GimsRuScraper = GimsRuScraper()
    gims_scraper.scrap(timestamp, dry_run=dry_run, requests_limit=requests_limit)

    # --- run scraper for rivreg.ru
    riv_scraper: RivRegRuScraper = RivRegRuScraper()
    riv_scraper.scrap(timestamp, dry_run=dry_run, requests_limit=requests_limit)

    # --- scraper class for morflot.ru
    morflot_scraper: MorflotRuScraper = MorflotRuScraper()
    morflot_scraper.scrap(timestamp, dry_run=dry_run, requests_limit=requests_limit)

    # --- scraper for rs-class.org
    # rs_scraper: RsClassOrgScraper = RsClassOrgScraper(const.SYSTEM_RSCLASSORG, const.SCRAPER_CACHE_PATH)
    # rs_scraper.scrap(dry_run=dry_run, requests_limit=requests_limit)

    # todo: implement the below scrapers properly!
    # # scraper class for vesselfinder.com
    # vf_scraper: VesselFinderComScraper = VesselFinderComScraper(const.SYSTEM_VESSELFINDERCOM,
    # const.SCRAPER_CACHE_PATH)
    # vf_scraper.scrap(dry_run=dry_run)
    # # scraper class for clarksons.net
    # # scraper class for marinetraffic.com
    # mtraffic_scraper: MarineTrafficComScraper = MarineTrafficComScraper(const.SYSTEM_MARINETRAFFICCOM,
    #                                                                     const.SCRAPER_CACHE_PATH)
    # mtraffic_scraper.scrap(dry_run=dry_run)
