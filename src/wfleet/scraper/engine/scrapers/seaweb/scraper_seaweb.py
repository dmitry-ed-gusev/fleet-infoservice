#!/usr/bin/env python3
# coding=utf-8

"""
    Data scraper for Sea Web database.
    Main data source address is https://maritime.ihs.com

    Created:  Gusev Dmitrii, 03.04.2022
    Modified: Gusev Dmitrii, 08.05.2022
"""

import os
import time
import random
import requests
import logging
from pathlib import Path
from typing import Set
from requests import Response
from wfleet.scraper.utils.utilities import read_file_as_text
from wfleet.scraper.config.scraper_config import Config, singleton, MSG_MODULE_ISNT_RUNNABLE
from wfleet.scraper.exceptions.scraper_exceptions import ScraperException

log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")

# base ship data URL
ship_url = 'https://maritime.ihs.com/Ships/Details/Index/'

# ship URLs for additional details
ship_additional_data_urls = {
    "ship_ownership": "https://maritime.ihs.com/Ships/OwnerAndRegistration/ShipOwnership/",
    "ship_ownership_history": "https://maritime.ihs.com/Ships/OwnerAndRegistration/ShipOwnershipHistory/",
    "ship_registration": "https://maritime.ihs.com/Ships/OwnerAndRegistration/ShipRegistration/",
    "safety": "https://maritime.ihs.com/Ships/SafetyAndCertification/SafetyAndCertificationOverviewAsync/",
    "class": "https://maritime.ihs.com/Ships/SafetyAndCertification/ClassAsync/",
    "class_surveys": "https://maritime.ihs.com/Ships/SafetyAndCertification/ClassSurveysAsync/",
    "crew": "https://maritime.ihs.com/Ships/SafetyAndCertification/CrewListAsync/",
    "inspections": "https://maritime.ihs.com/Ships/SafetyAndCertification/InspectionsAsync/",
    "safety_mgmt": "https://maritime.ihs.com/Ships/SafetyAndCertification/SafetyManagementAsync/",
    "safety_certs": "https://maritime.ihs.com/Ships/SafetyAndCertification/SafetyCertificatesAsync/",
    "casualty": "https://maritime.ihs.com/Ships/SafetyAndCertification/CasualtyAndEventsAsync/",
    "construction": "https://maritime.ihs.com/Ships/Construction/ConstructionOverview/",
    "alterations": "https://maritime.ihs.com/Ships/Construction/Alterations/",
    "arrangement": "https://maritime.ihs.com/Ships/Construction/ShipArrangement/",
    "construction_details": "https://maritime.ihs.com/Ships/Construction/ConstructionDetail/",
    "ship_disposal": "https://maritime.ihs.com/Ships/Construction/ShipDisposal/",
    "service_constr": "https://maritime.ihs.com/Ships/Construction/ServiceConstraints/",
    "ship_builder": "https://maritime.ihs.com/Ships/Construction/ShipBuilder/",
    "sisters": "https://maritime.ihs.com/Ships/Construction/Sisters/",
    "status_history": "https://maritime.ihs.com/Ships/Construction/StatusHistory/",
    "supplementary_features": "https://maritime.ihs.com/Ships/Construction/ShipSupplementaryFeatures/",
    "dimensions": "https://maritime.ihs.com/Ships/Dimensions/ShipDimensions/",
    "tonnages": "https://maritime.ihs.com/Ships/Dimensions/ShipTonnages/",
    "cargo": "https://maritime.ihs.com/Ships/CargoAndCapacities/CargoOverview/",
    "capacities": "https://maritime.ihs.com/Ships/CargoAndCapacities/Capacities/",
    "cargo_gear": "https://maritime.ihs.com/Ships/CargoAndCapacities/CargoGear/",
    "compartments": "https://maritime.ihs.com/Ships/CargoAndCapacities/Compartments/",
    "hatches": "https://maritime.ihs.com/Ships/CargoAndCapacities/Hatches/",
    "ro_ro": "https://maritime.ihs.com/Ships/CargoAndCapacities/RoRo/",
    "specialist": "https://maritime.ihs.com/Ships/CargoAndCapacities/Specialist/",
    "tanks": "https://maritime.ihs.com/Ships/CargoAndCapacities/Tanks/",
    "ocerview": "https://maritime.ihs.com/Ships/Machinery/OverviewAsync/",
    "aux_engines": "https://maritime.ihs.com/Ships/Machinery/AuxiliaryEnginesAsync/",
    "aux_generators": "https://maritime.ihs.com/Ships/Machinery/AuxiliaryGeneratorsAsync/",
    "boilers": "https://maritime.ihs.com/Ships/Machinery/BoilersAsync/",
    "bunkers": "https://maritime.ihs.com/Ships/Machinery/BunkersAsync/",
    "prime_mover": "https://maritime.ihs.com/Ships/Machinery/PrimeMoverDetailAsync/",
    "thrusters": "https://maritime.ihs.com/Ships/Machinery/ThrustersAsync/",
    "timeline": "https://maritime.ihs.com/Ships/Timeline/TimelineAsync/",
    # "photos": "https://maritime.ihs.com/Ships/Photographs/PhotographsAsync/",  # may be added later
    # "user_ship_note": "https://maritime.ihs.com/Ships/UserNote/GetUserShipNoteAsync/",  # may be added later
    # "inmarsat": "https://maritime.ihs.com/Ships/Links/InmarsatAsync/",  # may be added later
    # "equasis": "https://maritime.ihs.com/Ships/Links/Equasis/",  # may be added later
    # "ship_perf": "https://maritime.ihs.com/Ships/ShipPerformance/ShipPerformanceAsync/",  # may be added later
}

# ship builder base+additional details urls
ship_builder_urls = {
    "builder_base": "https://maritime.ihs.com/Builders/Details/",
    "builder_addresses": "https://maritime.ihs.com/Builders/Details/GetBuilderAddressesAsync/",
    "builder_history": "https://maritime.ihs.com/Builders/Details/GetBuilderHistoryAsync/",
    "builder_assoc": "https://maritime.ihs.com/Builders/Details/GetBuilderAssociationsAsync/",
    "builder_fleet": "https://maritime.ihs.com/Builders/Details/GetBuilderBuiltFleetAsync/",
    "builder_orders": "https://maritime.ihs.com/Builders/Details/GetBuilderOrderbookAsync/",
}

# ship company base + additional details urls
ship_company_additional_urls = {
    "company_base": "",
    "": "",
}

# session data - headers
session_headers = {
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "Upgrade-Insecure-Request": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36" \
                  "(KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8," \
              "application/signed-exchange;v=b3;q=0.9",
    "host": "maritime.ihs.com",

    # additional for extended data
    "Referer": "https://maritime.ihs.com/",
    "X-Requested-With": "XMLHttpRequest",

    # main header (cookie)
    "Cookie": "_ga=GA1.2.1607646022.1648412853; shipsearch=; ckShipDiv=hidehidehidehidehideshowhidehide; list=; ShipCommercialHistoryExpanded=ShipCommercialHistoryExpanded; ckShip=db_name001=VESSELNAMEBROWSE&en_name001=Name of Ship&db_name002=DATEOFBUILDBROWSE&en_name002=Built&db_name003=DWT&en_name003=Deadweight&db_name004=FLAG&en_name004=Flag&db_name005=STATUSBROWSE&en_name005=Status&db_name006=OWNER&en_name006=Registered Owner&db_name007=NBPriceUSDEquivalent&en_name007=Newbuilding Price&db_name008=EngineBuilderLargest&en_name008=Engine Builder&db_name009=EngineMakeLargest&en_name009=Engine Design&db_name010=SHIPBUILDER&en_name010=Shipbuilder&db_name011=BUILDERCODE&en_name011=Shipbuilder Code&db_name012=YEAROFBUILDBROWSE&en_name012=Year; rememberMeLogin=903C2E6ED95029E847A45CBBA806034E344A8D08EEF2BEF8D865B9ED17CBA4861D8A6A0A9E5BE8A9554EB3CB99E67FC0C86AFC7A28FB6FF17C42E6AB5FA3994FEDB6581C716DC1E3FD3EBC4E243BFC29E7482B1DF44D2BB481F2B5CFE124E693C44793BD0447CAF52DE7301D; LastShipVisited=1009340A+8009129DF 19+9237371WEC VERMEER+7920259ABDUL B+9237369MOVEON; ownersearch=; ckOwnDiv=hidehidehidehideshowhidehidehide; buildersearch=; ckBuilderDiv=hidehideshowhidehidehidehidehide; ckbuilder=db_name001=BUILDERNAME&en_name001=Builder Name&db_name002=COUNTRYNAME&en_name002=Country&db_name003=STATUS&en_name003=Status&db_name004=TOWNNAME&en_name004=Town; ckDefault=page=buildersearch&records=20; builderovw=; LastBuilderVisited=USAE95A & B Industries Of Morgan City+IRN030Abadan Kashti Nooh+JPN028Onomichi Dockyard Co Ltd; ASP.NET_SessionId=pmr4jdtsrcr2k4frsmrzyhen; SameSite=None; BIGipServer~ProdWeb~pool-maritime.ihs.com-80=rd1100o00000000000000000000ffff0aa80069o80; AttemptsToLogin=XwsNHfGK7AFvYICFRjPeuTyTLQUS8ALHuSVVs94kHgtsuuPB; .AspNet.ApplicationCookie=OQ4DAxTK8p5kDwIwRvcmE_Nyw2OAjDEeNjrKFi17h6_07Fhg7MmnpSlWIXrrWEgfE_u0CD30IjfddfWJgrTbSnX77WmDP9qnOilgttGs4MVSyeGCyo3n4pYzrCCRRTCSf35diFNzpNvJgcA-iJ4t7Xo4_iWhh2b2w9RvfSAC7nauT9Sy_nw7mE709Vq0htA8sdMPzmwO1c4QZBwn_OcR6WC71k9xcNMpwAZykkV1Kp_fcfXNF7AQHD5B4xWPcqjp7KKf665O8qAPaekrY8QHFehg3ZWM7c7mUvtbP6Hgu2P6__BNM7ThS-MMlRxyMuN5rwu74RznQzbb9I7B0YD7PYQvuxMNvN7PJhEjNVI6K-nR6YS16gaX-Ke56tGKKciiIqmVIZRMd774ndzgQNiyuE01fVZsFt1AbgXNiEAJnTf5DI3oMibZ471ZzM_0_z6udfFkH3jBs8aU9i8JUALwkuT0TeGKk9ES3kEGa7p-dkk2_lYwB_fIkqo_y12SpmUR5ygp60AsPE6xuyFu2ZBREMK9v3CUkk5uFyyGE22sveoJvej2; _gid=GA1.2.1476109304.1651695844; _gat=1; ADRUM_BT1=R:0|i:461009; ADRUM_BTa=R:0|g:9a6fc6b0-70be-4572-b237-ad6f0f20a6ab|n:ihsco_86f4fc53-86e8-4feb-bc7a-7921d526821f",
}

# session data - cookies
session_cookies: dict = {}

# setup HTTP session
# session = requests.Session()
# session.headers.update(session_headers)
# session.cookies.update(session_cookies)  # add cookies to session headers
# session.max_redirects = 100  # limit max redirects # to follow


@singleton
class WebClient():
    """Simple WebClient class."""

    def __init__(self, headers: dict, cookies: dict) -> None:
        log.debug("Initializing WebCLient() singleton instance.")
        self.headers = headers
        self.cookies = cookies
        self.session = requests.Session()

        if headers and len(headers) > 0:  # add headers
            self.session.headers.update(self.headers)
            log.debug("Headers are not empty, adding to the HTTP session.")

        if cookies and len(cookies) > 0:  # add cookies
            self.session.cookies.update(self.cookies)
            log.debug("Cookies are not empty, adding to the HTTP session.")

    def set_redirects_count(self, redirects_count: int):
        if redirects_count > 0:
            self.session.max_redirects = redirects_count

    def get_request(self, url: str, allow_redirects=True, fail_on_error=True) -> Response:
        log.debug(f"Performing get request: [{url}].")

        if not url:
            raise ScraperException("Empty URL for get request!")

        response = self.session.get(url, allow_redirects=allow_redirects)
        if response.status_code != 200 and fail_on_error:  # fail on purpose - by parameter
            raise ScraperException(f"Get request [{url}] failed with [{response.status_code}]!")

        return response

    def get_request_return_text(self, url: str, allow_redicrects: bool, fail_on_error: bool) -> str:
        return self.get_request(url, allow_redicrects, fail_on_error).text


config = Config()  # get app config instance
web_client = WebClient(session_headers, session_cookies)  # get web client instance


def scrap_base_ships_data(imo_numbers: Set[int],
                          req_limit: int = config.default_requests_limit,
                          req_delay: int = config.default_timeout_delay_max,
                          req_delay_cadence: int = config.default_timeout_cadence):

    log.debug("scrap_base_ships_data() is working.")

    if not imo_numbers or len(imo_numbers) == 0:  # fail-fast - empty IMO numbers list
        raise ScraperException("Empty IMO numbers list for processing!")

    for counter, imo_number in enumerate(imo_numbers):  # iterate over all IMO numbers

        if counter > 0 and counter % 1000 == 0:  # just a debug
            log.debug(f"Processing: {counter}/{len(imo_numbers)}.")

        if req_limit > 0 and counter > req_limit:  # just a stopper (sentinel)
            break

        ship_dir = config.seaweb_raw_ships_dir + "/" + str(imo_number)  # directory to store the current ship
        log.info(f'Ship: IMO #{imo_number}. Dir: [{ship_dir}].')

        if Path(ship_dir).exists() and Path(ship_dir).is_dir():  # skip already processed ships
            log.debug(f"Ship IMO: #{imo_number} already processed. Skipped.")
            continue

        # artificial delay for every 50 run
        if counter % req_delay_cadence == 0:
            delay_sec = random.randint(1, req_delay)  # delay 1 to X sec (both inclusive)
            log.debug(f"\tDelay {delay_sec} seconds.")
            time.sleep(delay_sec)

        # real ship processing
        text = web_client.get_request_return_text(ship_url + str(imo_number),
                                                  allow_redicrects=True,
                                                  fail_on_error=True)
        # response = session.get(ship_url + str(imo_number), allow_redirects=True)  # request the site...
        # if response.status_code != 200:  # check that 200 is returned
        #     log.error(f"Got error code: {response.status_code}! Stopping!")
        #     break

        os.makedirs(ship_dir, exist_ok=True)  # if all is OK - create dir for the ship data
        ship_data_file: str = ship_dir + '/' + config.main_ship_data_file
        with open(Path(ship_data_file), 'w') as f:  # write content to the file
            # f.write(response.text)
            f.write(text)
            log.debug(f"Written file: {ship_data_file}")

    log.info(f'Processed IMO numbers: {len(imo_numbers)}.')


def scrap_extended_ships_data(imo_numbers: Set[int],
                              req_limit: int = config.default_requests_limit,
                              req_delay: int = config.default_timeout_delay_max,
                              req_delay_cadence: int = config.default_timeout_cadence):

    log.debug("scrap_extended_ships_data() is working.")

    if not imo_numbers or len(imo_numbers) == 0:  # fail-fast - empty IMO numbers list
        raise ScraperException("Empty IMO numbers list for processing!")

    for counter, imo_number in enumerate(imo_numbers):  # iterate over all IMO numbers

        if counter > 0 and counter % 1000 == 0:  # just a debug
            log.debug(f"Processing: {counter}/{len(imo_numbers)}.")

        if req_limit > 0 and counter > req_limit:  # just a stopper (sentinel)
            break

        ship_dir = config.seaweb_raw_ships_dir + "/" + str(imo_number)  # directory to store the current ship
        log.info(f'Ship: IMO #{imo_number}. Dir: [{ship_dir}].')

        # check existence of several files with additional info and request it if missing
        skip_delay = True
        for key in ship_additional_data_urls:
            # print(f"key={key}, value={ship_additional_data_urls[key]}")
            ship_ext_file = ship_dir + "/" + key + ".html"
            if not Path(ship_ext_file).exists():
                # print(f"\tFile [{key}].html doesn't exist, downloading...")  # <- too much output
                skip_delay = False  # we're doing real requests, so need a delay
                text = web_client.get_request_return_text(ship_additional_data_urls[key] + str(imo_number),
                                                          allow_redicrects=True,
                                                          fail_on_error=True)
                # # download missing file
                # response = session.get(ship_additional_data_urls[key] + row[0])
                # # check that 200 is returned - break otherwise
                # if response.status_code != 200:
                #     print(f"Error code: {response.status_code} returned! Stopping!")
                #     return

                # save downloaded file if 200 OK returned
                with open(Path(ship_ext_file), 'w') as f:  # write received content to file
                    # f.write(response.text)
                    f.write(text)
                    log.debug(f"Written file: {ship_ext_file}")

        # artificial delay for every XX runs
        if not skip_delay and counter % req_delay_cadence == 0:
            delay_sec = random.randint(1, req_delay)  # delay 1 to X sec (both inclusive)
            log.debug(f"Delay {delay_sec} seconds.")
            time.sleep(delay_sec)

    log.debug(f'Processed IMO numbers {len(imo_numbers)}.')


def process_raw_data():
    ships_dirs = os.listdir(RAW_SHIPS_DIR)
    print(f"Total ships: {len(ships_dirs)}.")

    counter: int = 0
    # iterate over all dirs/ships and process data
    for ship in ships_dirs:

        if not ship.isnumeric():  # skip non-numeric dirs
            print(f"Found non-numeric object: [{ship}]")
            continue

        ship_data: str = read_file_as_text(RAW_SHIPS_DIR + "/" + ship + "/" + MAIN_SHIP_DATA_FILE)
        if "Access is denied." in ship_data:
            continue

        counter += 1

    print(f"Ships with data: {counter}")


def main(imo_file: str, imo_file_delim: str, processed_base_file: str, processed_ext_file: str):
    # scrap_base_data(imo_numbers_file=imo_file, imo_numbers_file_delimeter=imo_file_delim,
    #               processed_imo_numbers=processed_base_file)
    # scrap_extended_data(imo_numbers_file=imo_file, imo_numbers_file_delimeter=imo_file_delim,
    #                   processed_imo_numbers=processed_ext_file)
    # process_raw_data()

    data_file = os.getcwd() + "/temp/9336505/ship_main.html"
    ship_data = _parse_ship_main(read_file_as_text(data_file))
    print(ship_data)


if __name__ == '__main__':
    print(MSG_MODULE_ISNT_RUNNABLE)
