#!/usr/bin/env python3
# coding=utf-8

"""
    Data scraper for Sea Web database.
    Main data source address is https://maritime.ihs.com

    Created:  Gusev Dmitrii, 03.04.2022
    Modified: Gusev Dmitrii, 29.05.2022
"""

import os
import time
import random
import logging
import shutil
from pathlib import Path
from typing import Set
from wfleet.scraper.utils.utilities import read_file_as_text
from wfleet.scraper.config.scraper_config import Config
from wfleet.scraper.utils.utilities_http import WebClientSingleton
from wfleet.scraper.config.scraper_messages import MSG_MODULE_ISNT_RUNNABLE
from wfleet.scraper.exceptions.scraper_exceptions import ScraperException
from wfleet.scraper.utils.codes_engine import CodesProcessor, CodesProcessorFactory
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
    "company_base": "https://maritime.ihs.com/Companies/Details/",
    "company_contacts": "https://maritime.ihs.com/Companies/Details/CompanyContactsAsync/",
    "company_address": "https://maritime.ihs.com/Companies/Details/CompanyAddressAsync/",
    "company_group": "https://maritime.ihs.com/Companies/Details/CompanyGroupAsync/",
    "related_companies": "https://maritime.ihs.com/Companies/Details/CompanyRelatedCompaniesAsync/",
    "company_history": "https://maritime.ihs.com/Companies/Details/CompanyHistoryAsync/",
    "company_notes": "https://maritime.ihs.com/Companies/Note/GetCompanyNotesAsync/",
    "fleet_size": "https://maritime.ihs.com/Companies/Fleet/GetFleetSizeAsync/",
    "combined_fleet": "https://maritime.ihs.com/Companies/Fleet/GetCompanyCombinedFleetAsync/",
    "doc_holder": "https://maritime.ihs.com/Companies/Fleet/GetCompanyDOCHolderFleetAsync/",
    "company_group_fleet": "https://maritime.ihs.com/Companies/Fleet/GetCompanyGroupFleetAsync/",
    "ship_manager_fleet": "https://maritime.ihs.com/Companies/Fleet/GetCompanyShipManagerFleetAsync/",
    "operated_fleet": "https://maritime.ihs.com/Companies/Fleet/GetCompanyOperatedFleetAsync/",
    "registered_owner_fleet": "https://maritime.ihs.com/Companies/Fleet/GetCompanyRegisteredOwnerFleetAsync/",
    "tech_manager_fleet": "https://maritime.ihs.com/Companies/Fleet/GetCompanyTechnicalManagerFleetAsync/",
    "historical_fleet": "https://maritime.ihs.com/Companies/Fleet/GetCompanyHistoricalFleetAsync/",
    "fleet_positions": "https://maritime.ihs.com/Companies/FleetMovements/GetCompanyFleetPositionsAsync/",
    "fleet_trading_areas": "https://maritime.ihs.com/Companies/FleetMovements/GetCompanyFleetTradingAreasAsync/",
    "company_casuaties": "https://maritime.ihs.com/Companies/CasualtyAndEvents/GetCompanyCasualtiesByIdAsync/",
    "historical_fleets_by_id": "https://maritime.ihs.com/Companies/CasualtyAndEvents/GetCompanyHistoricalFleetsByIdAsync/",
    "doc_certificates": "https://maritime.ihs.com/Companies/Certification/GetCompanyDocCertificatesAsync/",
    "cert_inspections": "https://maritime.ihs.com/Companies/Certification/GetCompanyCertInspectionsAsync/",
    "company_inspections_history": "https://maritime.ihs.com/Companies/Certification/GetCompanyInspectionsHistoryAsync/",
    "company_benchmark": "https://maritime.ihs.com/Companies/Benchmark/GetCompanyBenchmarkAsync/",
    "company_notes_2": "https://maritime.ihs.com/Companies/Note/GetUserCompanyNoteAsync/5451458",
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
    "Cookie": "_ga=GA1.2.1607646022.1648412853; shipsearch=; ckShipDiv=hidehidehidehidehideshowhidehide; list=; ShipCommercialHistoryExpanded=ShipCommercialHistoryExpanded; ckShip=db_name001=VESSELNAMEBROWSE&en_name001=Name of Ship&db_name002=DATEOFBUILDBROWSE&en_name002=Built&db_name003=DWT&en_name003=Deadweight&db_name004=FLAG&en_name004=Flag&db_name005=STATUSBROWSE&en_name005=Status&db_name006=OWNER&en_name006=Registered Owner&db_name007=NBPriceUSDEquivalent&en_name007=Newbuilding Price&db_name008=EngineBuilderLargest&en_name008=Engine Builder&db_name009=EngineMakeLargest&en_name009=Engine Design&db_name010=SHIPBUILDER&en_name010=Shipbuilder&db_name011=BUILDERCODE&en_name011=Shipbuilder Code&db_name012=YEAROFBUILDBROWSE&en_name012=Year; rememberMeLogin=903C2E6ED95029E847A45CBBA806034E344A8D08EEF2BEF8D865B9ED17CBA4861D8A6A0A9E5BE8A9554EB3CB99E67FC0C86AFC7A28FB6FF17C42E6AB5FA3994FEDB6581C716DC1E3FD3EBC4E243BFC29E7482B1DF44D2BB481F2B5CFE124E693C44793BD0447CAF52DE7301D; LastShipVisited=1009340A+8009129DF 19+9237371WEC VERMEER+7920259ABDUL B+9237369MOVEON; ownersearch=; ckOwnDiv=hidehidehidehideshowhidehidehide; buildersearch=; ckBuilderDiv=hidehideshowhidehidehidehidehide; ckbuilder=db_name001=BUILDERNAME&en_name001=Builder Name&db_name002=COUNTRYNAME&en_name002=Country&db_name003=STATUS&en_name003=Status&db_name004=TOWNNAME&en_name004=Town; ckDefault=page=buildersearch&records=20; builderovw=; BIGipServer~ProdWeb~pool-maritime.ihs.com-80=rd1100o00000000000000000000ffff0aa8006ao80; _gid=GA1.2.1781089551.1653858578; LastBuilderVisited=USAE95A & B Industries Of Morgan City+IRN030Abadan Kashti Nooh+JPN028Onomichi Dockyard Co Ltd+MAL094Natah Shipyard Sdn Bhd; ASP.NET_SessionId=cyw1gy5qteyusnsivaacm3mo; SameSite=None; AttemptsToLogin=DxLDUXHf8r3htUMqYNwBkwdRpKGnWB/DocxOsgZKDmOFRZHu; .AspNet.ApplicationCookie=h3M1zOkeI8I-7V9hvY10vqJu1iIAopoDVPeCNer5hqj4MJwPrs6vekp07UW8zDNZ4Ubr1_cO0dkvsi4WKJN7_uNcuAoPj0jzWUTSQ15JlNdKQjPptmoqNjayI3s0oPSWUsZPZkGqcub3MdAqDZ1RkuKlV30FHeY1GaSkWJD_LkT-uKUi6aISixe93DRFwidzrsaihEamYPapVvEo2m3ZDIKPmZ2La96QJScgg5mWbJfqnuTNIjsjy-YXQm8eLqdLOTh2CTEHLc8ZsA6_0huJzg_447Bm6KrBLqOLjiaURCLfE6-kY-W9-dwO2uFrT3bAcY51lK5n-__XlRVRRFAintIGlYWlL6FvRe0XjDy4ulQy_X8PLb0R2EZCN_b3aC6qYokK5TAGyGDpVFIffzMs4K96PpCFtYfGiBeUywR9mcUcWveuvX8HUgr41y1sR-DETKv40pLzXfcl32KKQrjPgtCtoRPXNOVL51WRlSssZabIF8sxJWbOYep3eAbUKg6UjfxeWDRdq6coIi9zAWfDlSY_cYeKXedhHJFQTicRAEx5DbAZcjFv7_MG3RY; _gat=1",
}

session_cookies: dict = {}  # session data - cookies
config = Config()  # get app config instance
web_client = WebClientSingleton(session_headers, session_cookies)  # get web client instance


def scrap_base_ships_data(imo_numbers: Set[str],
                          req_limit: int = config.default_requests_limit,
                          req_delay: int = config.default_timeout_delay_max,
                          req_delay_cadence: int = config.default_timeout_cadence):

    log.debug("scrap_base_ships_data() is working.")

    if not imo_numbers or len(imo_numbers) == 0:  # fail-fast - empty IMO numbers list
        raise ScraperException("Empty IMO numbers list for processing!")

    imo_numbers_length = len(imo_numbers)
    for counter, imo_number in enumerate(imo_numbers):  # iterate over all IMO numbers

        # if counter > 0 and counter % 1000 == 0:  # just a debug
        #     log.debug(f"Processing: {counter}/{len(imo_numbers)}.")

        if req_limit > 0 and counter > req_limit:  # just a stopper (sentinel)
            break

        ship_dir = config.seaweb_raw_ships_dir + "/" + str(imo_number)  # directory to store the current ship
        log.info(f'Ship: IMO #{imo_number} ({counter}/{imo_numbers_length}). Dir: [{ship_dir}].')

        if Path(ship_dir).exists() and Path(ship_dir).is_dir():  # skip already processed ships
            # log.debug(f"Ship IMO: #{imo_number} already processed. Skipped.")
            continue

        # artificial delay for every XXX runs
        if counter % req_delay_cadence == 0:
            delay_sec = random.randint(1, req_delay)  # delay 1 to X sec (both inclusive)
            log.debug(f"\tDelay {delay_sec} seconds.")
            time.sleep(delay_sec)

        # real ship processing (create dirs/make name for data file/get file data by HTTP GET request)
        os.makedirs(ship_dir, exist_ok=True)  # if all is OK - create dir for the ship data
        ship_data_file: str = ship_dir + '/' + config.main_ship_data_file  # create ship data file name
        web_client.get_request_return_text_to_file(ship_url + str(imo_number), ship_data_file,
                                                   allow_redicrects=True, fail_on_error=True)

    log.info(f'Processed IMO numbers: {imo_numbers_length}.')


def scrap_extended_ships_data(imo_numbers: Set[str],
                              req_limit: int = config.default_requests_limit,
                              req_delay: int = config.default_timeout_delay_max,
                              req_delay_cadence: int = config.default_timeout_cadence):

    log.debug("scrap_extended_ships_data() is working.")

    if not imo_numbers or len(imo_numbers) == 0:  # fail-fast - empty IMO numbers list
        raise ScraperException("Empty IMO numbers list for processing!")

    imo_numbers_length = len(imo_numbers)
    for counter, imo_number in enumerate(imo_numbers):  # iterate over all IMO numbers

        # if counter > 0 and counter % 1000 == 0:  # just a debug
        #     log.debug(f"Processing: {counter}/{len(imo_numbers)}.")

        if req_limit > 0 and counter > req_limit:  # just a stopper (sentinel)
            break

        ship_dir = config.seaweb_raw_ships_dir + "/" + str(imo_number)  # directory to store the current ship
        log.info(f'Ship: IMO #{imo_number} ({counter}/{imo_numbers_length}). Dir: [{ship_dir}].')

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

    log.debug(f'Processed IMO numbers: {imo_numbers_length}.')


def _build_ship_builders_and_companies_codes(delete_invalid=False) -> None:
    log.debug("_build_ship_builders_and_companies_codes() is working.")

    ships_dirs_list: list[str] = os.listdir(config.seaweb_raw_ships_dir)
    log.debug(f"Found total ships/directories: {len(ships_dirs_list)}.")

    # main processing cycle
    shipbuilders: CodesProcessor = CodesProcessorFactory.seaweb_shipbuildes_codes()
    shipcompanies: CodesProcessor = CodesProcessorFactory.seaweb_shipcompanies_codes()
    invalid_ships: Set[str] = set()  # set of invalid ships (wrong info)
    for counter, ship in enumerate(ships_dirs_list):  # iterate over all dirs/ships and process data
        log.debug(f'Currently processing: {ship} ({counter}/{len(ships_dirs_list)})')

        if not ship.isnumeric():  # skip non-numeric dirs
            log.warning(f"Skipped the current number [{ship}] - non-numeric object!")
            continue

        # check - if we can parse this ship - raw info file contains 'Access is denied.'
        ship_dir: str = config.seaweb_raw_ships_dir + "/" + ship  # ship directory
        ship_main_file: str = ship_dir + "/" + config.main_ship_data_file  # ship main file
        ship_data: str = read_file_as_text(ship_main_file)
        if "Access is denied." in ship_data:
            log.warning(f"Skipped the current number [{ship}] - no data (Access is denied)!")
            continue

        # get parsed ship dictionary
        ship_dict: dict = _parse_ship_main(ship_data, interest_keys={'Operator', 'Shipbuilder'})

        # get ship builder code
        builder_code: str = ship_dict.get('ship_builder_seaweb_id', 'x')
        if builder_code != '-' and builder_code != 'x':  # shipbuilder code is OK
            shipbuilders.add(builder_code)
            log.debug(f'Added ship builder code: {builder_code}')
        elif builder_code == '-':  # builder code not found in the ship
            log.warn(f'Ship builder code not found for: {ship}!')
        elif builder_code == 'x':  # builder code key not in the ship - invalid ship info!
            log.error(f'Found invalid ship data for: {ship}!')
            invalid_ships.add(ship)
            if delete_invalid:  # if key is set - remove invalid ship folder
                log.warn(f'Deleting: [{ship_dir}]!')
                shutil.rmtree(ship_dir, ignore_errors=True)  # remove directory with invalid ship data

        # get ship operator code
        operator_code: str = ship_dict.get('ship_operator_seaweb_id', 'x')
        if operator_code != '-' and operator_code != 'x':  # shipoperator code is OK
            shipcompanies.add(operator_code)
            log.debug(f'Added ship operator code: {operator_code}')
        elif operator_code == '-':  # operator code not found in the ship
            log.warn(f'Ship operator code not found for: {ship}!')
        elif operator_code == 'x':  # operator code not in the ship - invalid ship info!
            log.error(f'Found invalid ship data for: {ship}!')
            invalid_ships.add(ship)
            if delete_invalid:  # if key is set - remove invalid ship folder
                log.warn(f'Deleting: [{ship_dir}]!')
                shutil.rmtree(ship_dir, ignore_errors=True)  # remove directory with invalid ship data

    if len(invalid_ships) > 0:  # if there were invalid ships - put info to the console
        log.warn(f'Fould invalid ships: {invalid_ships}!')


def scrap_shipbuilders_data(req_limit: int = config.default_requests_limit,
                            req_delay: int = config.default_timeout_delay_max,
                            req_delay_cadence: int = config.default_timeout_cadence):
    log.debug("scrap_shipbuilders_data() is working.")

    # go through the codes and scrap necessary data
    shipbuilders: CodesProcessor = CodesProcessorFactory.seaweb_shipbuildes_codes()

    shipbuilders_length = len(shipbuilders.codes())
    for counter, shipbuilder in enumerate(shipbuilders.codes()):  # iterate over shipbuilders codes

        if req_limit > 0 and counter > req_limit:  # just a stopper (sentinel)
            break

        # directory to store the current shipbuilder
        shipbuilder_dir = config.seaweb_raw_builders_dir + "/" + str(shipbuilder)
        log.info(f'Shipbuilder: #{shipbuilder} ({counter}/{shipbuilders_length}). Dir: [{shipbuilder_dir}].')
        os.makedirs(shipbuilder_dir, exist_ok=True)  # if all is OK - create dir for the ship data

        # check existence of several files with additional info and request it if missing
        skip_delay = True
        for key in ship_builder_urls:
            shipbuilder_file = shipbuilder_dir + "/" + key + ".html"
            if not Path(shipbuilder_file).exists():
                skip_delay = False  # we're doing real requests, so need a delay
                # HTTP GET request + save to file
                web_client.get_request_return_text_to_file(ship_builder_urls[key] + str(shipbuilder),
                                                           shipbuilder_file,
                                                           allow_redicrects=True,
                                                           fail_on_error=True)

        # artificial delay for every XX runs
        if not skip_delay and counter % req_delay_cadence == 0:
            delay_sec = random.randint(1, req_delay)  # delay 1 to X sec (both inclusive)
            log.debug(f"Delay {delay_sec} seconds.")
            time.sleep(delay_sec)

    log.debug(f'Processed Ship Builders: {shipbuilders_length}.')


def scrap_shipoperators_data():
    log.debug("scrap_shipoperators_data() is working.")
    # go through the codes and scrap necessary data


if __name__ == '__main__':
    print(MSG_MODULE_ISNT_RUNNABLE)
