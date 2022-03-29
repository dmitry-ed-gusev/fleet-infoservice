#!/usr/bin/env python3
# coding=utf-8

"""
    Scraper Engine Module. Manage all scraper operations. Should'n be called
    directly - rather should be imported and functions used.

    Created:  Dmitrii Gusev, 24.12.2021
    Modified: Dmitrii Gusev, 29.03.2022
"""

# todo: add DB support for scraper runs telemetry
# todo: add execution time measurement for particular scrapers

import logging
from datetime import datetime
from wfleet.scraper.config.scraper_config import CONFIG
from wfleet.scraper.config.scraper_config import MSG_MODULE_ISNT_RUNNABLE
from wfleet.scraper.engine.scrapers.scraper_clarksonsnet import ClarksonsNetScraper
from wfleet.scraper.engine.scrapers.scraper_gims import GimsRuScraper
from wfleet.scraper.engine.scrapers.scraper_rivregru import RivRegRuScraper
from wfleet.scraper.engine.scrapers.scraper_morflotru import MorflotRuScraper
from wfleet.scraper.engine.scrapers.scraper_marinetrafficcom import MarineTrafficComScraper
from wfleet.scraper.engine.scrapers.scraper_vesselfindercom import VesselFinderComScraper

# init module logging
log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")


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

    # --- run scraper for marinetraffic.com
    mtraffic_scraper: MarineTrafficComScraper = MarineTrafficComScraper()
    mtraffic_scraper.scrap(timestamp, dry_run=dry_run, requests_limit=requests_limit)

    # --- run scraper for vesselfinder.com
    vf_scraper: VesselFinderComScraper = VesselFinderComScraper()
    vf_scraper.scrap(timestamp, dry_run=dry_run, requests_limit=requests_limit)

    # --- scraper for rs-class.org
    # rs_scraper: RsClassOrgScraper = RsClassOrgScraper(const.SYSTEM_RSCLASSORG, const.SCRAPER_CACHE_PATH)
    # rs_scraper.scrap(dry_run=dry_run, requests_limit=requests_limit)


# main part of the script
if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
