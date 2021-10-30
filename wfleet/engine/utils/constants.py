# coding=utf-8

"""
    Useful scraper constants, shared between multiple modules / scripts.

    Created:  Gusev Dmitrii, 28.05.2021
    Modified: Dmitrii Gusev, 20.06.2021
"""

# general configuration
DEFAULT_ENCODING = "utf-8"
SCRAPER_CACHE_PATH = "./engine/cache"
SCRAPER_CACHE_DIRECTORY_TIMESTAMP_PATTERN = (
    "%d-%b-%Y_%H-%M-%S"  # timestamp without fractions
)
SCRAPER_CACHE_DRY_RUN_DIR_SUFFIX = "-dryrun"
SCRAPER_CACHE_LIMITED_RUN_DIR_SUFFIX = "-requests-limited"
TIMEOUT_URLLIB_URLOPEN: int = (
    12 * 60 * 60
)  # timeout is set in seconds (?) - 12h (currently)

# systems names + logging configuration (system name is used as a logger name as well)
LOGGING_CONFIG_FILE = "logging.yml"

LOGGING_SCRAPER_PROCESSOR_LOGGER = "fleet_scraper"
LOGGING_SCRAPER_ARCHIVER_LOGGER = "fleet_scrape_archiver"
LOGGING_UTILITIES_LOGGER = "scraper_utilities"
LOGGING_UTILITIES_XLS_LOGGER = "scraper_utilities_xls"
LOGGING_UTILITIES_HTTP_LOGGER = "scraper_utilities_http"

SYSTEM_RSCLASSORG = "scraper_rsclassorg"
SYSTEM_RIVREGRU = "scraper_rivregru"
SYSTEM_MORFLOTRU = "scraper_morflotru"
SYSTEM_GIMS = "scraper_gims"
SYSTEM_VESSELFINDERCOM = "scraper_vesselfindercom"
SYSTEM_MARINETRAFFICCOM = "scraper_marinetrafficcom"
SYSTEM_CLARKSONSNET = "scraper_clarksonsnet"

# scrap resulting excel files
EXCEL_SHIPS_DATA = "ships_data.xls"
# EXCEL_EXTENDED_SHIPS_DATA = 'extended_ships_data.xls'  # todo: do we need it?
EXCEL_DEFAULT_SHEET_NAME = "ships"
EXCEL_DEFAULT_TIMESTAMP_PATTERN = "%d-%b-%Y %H:%M:%S"

if __name__ == "__main__":
    print("Don't run this constants script directly!")
