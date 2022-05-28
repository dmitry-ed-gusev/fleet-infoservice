#!/usr/bin/env python3
# coding=utf-8

"""
    Data scraper for Sea Web database.
    Main data source address is https://maritime.ihs.com

    Created:  Gusev Dmitrii, 03.04.2022
    Modified: Gusev Dmitrii, 18.05.2022
"""

import os
import csv
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
from wfleet.scraper.engine.scrapers.seaweb.parser_seaweb import _parse_ship_main

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
    "Cookie": "_ga=GA1.2.1607646022.1648412853; shipsearch=; ckShipDiv=hidehidehidehidehideshowhidehide; list=; ShipCommercialHistoryExpanded=ShipCommercialHistoryExpanded; ckShip=db_name001=VESSELNAMEBROWSE&en_name001=Name of Ship&db_name002=DATEOFBUILDBROWSE&en_name002=Built&db_name003=DWT&en_name003=Deadweight&db_name004=FLAG&en_name004=Flag&db_name005=STATUSBROWSE&en_name005=Status&db_name006=OWNER&en_name006=Registered Owner&db_name007=NBPriceUSDEquivalent&en_name007=Newbuilding Price&db_name008=EngineBuilderLargest&en_name008=Engine Builder&db_name009=EngineMakeLargest&en_name009=Engine Design&db_name010=SHIPBUILDER&en_name010=Shipbuilder&db_name011=BUILDERCODE&en_name011=Shipbuilder Code&db_name012=YEAROFBUILDBROWSE&en_name012=Year; rememberMeLogin=903C2E6ED95029E847A45CBBA806034E344A8D08EEF2BEF8D865B9ED17CBA4861D8A6A0A9E5BE8A9554EB3CB99E67FC0C86AFC7A28FB6FF17C42E6AB5FA3994FEDB6581C716DC1E3FD3EBC4E243BFC29E7482B1DF44D2BB481F2B5CFE124E693C44793BD0447CAF52DE7301D; LastShipVisited=1009340A+8009129DF 19+9237371WEC VERMEER+7920259ABDUL B+9237369MOVEON; ownersearch=; ckOwnDiv=hidehidehidehideshowhidehidehide; buildersearch=; ckBuilderDiv=hidehideshowhidehidehidehidehide; ckbuilder=db_name001=BUILDERNAME&en_name001=Builder Name&db_name002=COUNTRYNAME&en_name002=Country&db_name003=STATUS&en_name003=Status&db_name004=TOWNNAME&en_name004=Town; ckDefault=page=buildersearch&records=20; builderovw=; LastBuilderVisited=USAE95A & B Industries Of Morgan City+IRN030Abadan Kashti Nooh+JPN028Onomichi Dockyard Co Ltd; ASP.NET_SessionId=144en2qq3h3m4h0z1exfqtfs; BIGipServer~ProdWeb~pool-maritime.ihs.com-80=rd1100o00000000000000000000ffff0aa80069o80; SameSite=None; AttemptsToLogin=O0H36qXSUP2UNgEXSnOtAkt2uc8iFw6l8PeOlJ4obVGWYRuC; .AspNet.ApplicationCookie=DApyVGx0cHKMePgWYt_dZpkqjocIJjghwrwRUNKRe7JWQd-dWctKvTT49DCgvyusrgT_BRjtwkuyqGktgFPcfWqLXgL0cpEztarfvY9pOnombM83mVs0-_F-dIkHHOWmqA9EsExyGdc78eSO-nzhq9BJmm0b-tMmrCODxl1dxlsaDBlvsKgspRbzUecWWAzGWYUhNayj8VobxKwETubgsijQrHOMaIi7_bba4OHJqb1h5Nx21OV8lp07pCeem01HSft0MSyKQ97OCf3p_rpoLhbfxXpjxjxxv4bAOjfRVQJrb5JX2B1KUJ4gZDQH-pyzxn1FmP8upCBd7gQ4s81eyxhWyzzr0HaLUj8e2VWbsk0e-kMeYKSj9_M5cI7826bhm7VjwVes9ACHMMXfnFdPzOb1mv8cE3JUo0pa9LT9fVX9EyfimsOhnS8KGLauC9k0QmtjDTQ-VuYvCPf_xwJnMtjuwHIma_OW8ptKpNp1c0lFPe37gcQsodeZWXlQUAAR_oSrhWB-T-zQzym7tkhmYDdiqqNAcBTk21Bkvg-xEgoIlpEnSmpEwenh0Io; _gid=GA1.2.1396874235.1652908372; _gat=1; ADRUM_BTa=R:0|g:9ca1bb55-1346-4153-86e7-2bb457546ba4|n:ihsco_86f4fc53-86e8-4feb-bc7a-7921d526821f; ADRUM_BT1=R:0|i:462877|e:1",
}

# session data - cookies
session_cookies: dict = {}

# setup HTTP session
# session = requests.Session()
# session.headers.update(session_headers)
# session.cookies.update(session_cookies)  # add cookies to session headers
# session.max_redirects = 100  # limit max redirects # to follow


@singleton
class WebClientSingleton():  # todo: move to utilities class!
    """Simple WebClient Singleton class."""

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
        log.debug(f"get_request(): performing get request: [{url}].")

        if not url:
            raise ScraperException("Empty URL for get request!")

        response = self.session.get(url, allow_redirects=allow_redirects)
        if response.status_code != 200 and fail_on_error:  # fail on purpose - by parameter
            raise ScraperException(f"Get request [{url}] failed with [{response.status_code}]!")

        return response

    def get_request_return_text(self, url: str, allow_redicrects: bool, fail_on_error: bool) -> str:
        log.debug('get_request_return_text(): working.')
        response = self.get_request(url, allow_redicrects, fail_on_error)
        if response:
            return response.text

        return ''

    def get_request_return_text_to_file(self, url: str, file: str, allow_redicrects: bool,
                                        fail_on_error: bool):
        log.debug(f'get_request_return_text_to_file(): saving response text to file {file}.')

        if not file or Path(file).exists():
            raise ScraperException(f'File name {file} is empty or file already exists!')

        response_text: str = self.get_request_return_text(url, allow_redicrects, fail_on_error)
        if response_text:
            with open(Path(file), 'w') as f:  # write content to the file
                f.write(response_text)
                log.debug(f"Written file: {file}")


config = Config()  # get app config instance
web_client = WebClientSingleton(session_headers, session_cookies)  # get web client instance


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

        # real ship processing (create dirs/make name for data file/get file data by HTTP GET request)
        os.makedirs(ship_dir, exist_ok=True)  # if all is OK - create dir for the ship data
        ship_data_file: str = ship_dir + '/' + config.main_ship_data_file  # create ship data file name
        web_client.get_request_return_text_to_file(ship_url + str(imo_number), ship_data_file,
                                                   allow_redicrects=True, fail_on_error=True)

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
            ship_ext_file = ship_dir + "/" + key + ".html"
            if not Path(ship_ext_file).exists():
                skip_delay = False  # we're doing real requests, so need a delay
                # HTTP GET request + save to file
                web_client.get_request_return_text_to_file(ship_additional_data_urls[key] + str(imo_number),
                                                           ship_ext_file,
                                                           allow_redicrects=True,
                                                           fail_on_error=True)

        # artificial delay for every XX runs
        if not skip_delay and counter % req_delay_cadence == 0:
            delay_sec = random.randint(1, req_delay)  # delay 1 to X sec (both inclusive)
            log.debug(f"Delay {delay_sec} seconds.")
            time.sleep(delay_sec)

    log.debug(f'Processed IMO numbers {len(imo_numbers)}.')


def _build_ship_builders_and_operators_codes_files() -> None:
    log.debug("_build_shipbuilders_codes_file() is working.")

    ships_dirs_list: list[str] = os.listdir(config.seaweb_raw_ships_dir)
    log.debug(f"Found total ships/directories: {len(ships_dirs_list)}.")

    shipbuilders: set = set()  # set for collecting ship builders codes
    shipoperators: set = set()  # set for collecting ship operators codes
    invalid_ships: set = set()  # set of invalid ships (wrong info)

    for counter, ship in enumerate(ships_dirs_list):  # iterate over all dirs/ships and process data

        log.debug(f'Currently processing: {ship} ({counter}/{len(ships_dirs_list)})')

        if not ship.isnumeric():  # skip non-numeric dirs
            log.warning(f"Skipped the current number [{ship}] - non-numeric object!")
            continue

        ship_main_file: str = config.seaweb_raw_ships_dir + "/" + ship + "/" + config.main_ship_data_file

        # check - if we can parse this ship
        ship_data: str = read_file_as_text(ship_main_file)
        if "Access is denied." in ship_data:
            log.warning(f"Skipped the current number [{ship}] - no data (Access is denied)!")
            continue

        # get parsed ship dictionary
        ship_dict: dict = _parse_ship_main(ship_data, interest_keys={'Operator', 'Shipbuilder'})

        # get ship builder code
        builder_code: str = ship_dict.get('ship_builder_seaweb_id', 'x')
        if builder_code != '-' and builder_code != 'x':
            shipbuilders.add(builder_code)
            log.debug(f'Added ship builder code: {builder_code}')
        elif builder_code == 'x':
            log.warn(f'Found wrong ship info for: {ship}!')
            invalid_ships.add(ship)

        # get ship operator code
        operator_code: str = ship_dict.get('ship_operator_seaweb_id', 'x')
        if operator_code != '-' and operator_code != 'x':
            shipoperators.add(operator_code)
            log.debug(f'Added ship operator code: {operator_code}')
        elif operator_code == 'x':
            log.warn(f'Found wrong ship info for: {ship}!')
            invalid_ships.add(ship)

    # write codes list to files - ship builders
    ship_builders_file: str = config.seaweb_raw_builders_dir + "/shipbuilders.csv"
    with open(ship_builders_file, mode='w') as file:
        csv_writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Ship Builder Code', 'Status'])  # write header row
        for shipbuilder in sorted(shipbuilders):  # write data to file
            csv_writer.writerow([shipbuilder, '+'])

    # write codes list to files - ship operators
    ship_operators_file: str = config.seaweb_raw_companies_dir + "/shipoperators.csv"
    with open(ship_operators_file, mode='w') as file:
        csv_writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Ship Operator Code', 'Status'])  # write header row
        for shipoperator in sorted(shipoperators):  # write data to file
            csv_writer.writerow([shipoperator, '+'])

    # print(f'shipbuilders -> {shipbuilders}')
    # print(f'shipoperators -> {shipoperators}')
    print(f'invalid ships -> {invalid_ships}')


def scrap_shipbuilders_data():
    log.debug("scrap_shipbuilders_data() is working.")
    # go through the codes and scrap necessary data


def scrap_shipoperators_data():
    log.debug("scrap_shipoperators_data() is working.")
    # go through the codes and scrap necessary data


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


if __name__ == '__main__':
    print(MSG_MODULE_ISNT_RUNNABLE)
