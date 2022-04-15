#!/usr/bin/env python3
# coding=utf-8

"""
    Data scraper for Sea Web database. Main data source address is https://maritime.ihs.com

    Created:  Gusev Dmitrii, 03.04.2022
    Modified: Gusev Dmitrii, 15.04.2022
"""

import os
import click
import csv
import time
import random
import requests
from pathlib import Path
from bs4 import BeautifulSoup

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
    "Cookie": "_ga=GA1.2.1607646022.1648412853; shipsearch=; ckShipDiv=hidehidehidehidehideshowhidehide; ckDefault=page=shipsearch&records=20; list=; ShipCommercialHistoryExpanded=ShipCommercialHistoryExpanded; ckShip=db_name001=VESSELNAMEBROWSE&en_name001=Name of Ship&db_name002=DATEOFBUILDBROWSE&en_name002=Built&db_name003=DWT&en_name003=Deadweight&db_name004=FLAG&en_name004=Flag&db_name005=STATUSBROWSE&en_name005=Status&db_name006=OWNER&en_name006=Registered Owner&db_name007=NBPriceUSDEquivalent&en_name007=Newbuilding Price&db_name008=EngineBuilderLargest&en_name008=Engine Builder&db_name009=EngineMakeLargest&en_name009=Engine Design&db_name010=SHIPBUILDER&en_name010=Shipbuilder&db_name011=BUILDERCODE&en_name011=Shipbuilder Code&db_name012=YEAROFBUILDBROWSE&en_name012=Year; rememberMeLogin=903C2E6ED95029E847A45CBBA806034E344A8D08EEF2BEF8D865B9ED17CBA4861D8A6A0A9E5BE8A9554EB3CB99E67FC0C86AFC7A28FB6FF17C42E6AB5FA3994FEDB6581C716DC1E3FD3EBC4E243BFC29E7482B1DF44D2BB481F2B5CFE124E693C44793BD0447CAF52DE7301D; BIGipServer~ProdWeb~pool-maritime.ihs.com-80=rd1100o00000000000000000000ffff0aa8006bo80; LastShipVisited=1009340A+8009129DF 19+9237371WEC VERMEER+7920259ABDUL B+9237369MOVEON; _gid=GA1.2.254984490.1649579321; ASP.NET_SessionId=cuhf5vw5htiyjgm5oakzfows; SameSite=None; .AspNet.ApplicationCookie=4VI95rU2G3rXizTMD4Yl5oQ9LyTwyfYDqGI5QKeELKg4aSI7IrrydWe4Om-GfRQf4WSsg13AiUreHjf8pIyDyaEh3ankl8WauGvKw3TbpD9N4SWU8vJpHr5A9u-3-FaToT11fLMgwshtvtSqLH4JRiCsakyM9NrgGSSy1hdzNzOq6yxPpHnSO5L6cD6OmG-p54qcMQ7lvLAAyQY6Gal1jesbZR46Ms-hYpDqjcSRCc_7ZB93MIjYyl5dV23HNEWtn9XW-k6mBJg_gwMWQ90ylTajqMB8xVl8L0qR8so3Nkje_h85BXU9UXa4I_Xxt_ymj0fIjQ8G6bO6oiM0Jdt9MfaHdWm3Qi-kQ8G2Y53cfRo8TGFbO_Jt9XTZKxekT6awwyRYvi9BKhmYEqi6Wc64cfXwEYURqslh5cAOZhjihGnPGFeLttUqQds6p09EQ_tmwnbMnRLdVA7raJFgzEZVKvHrfE_0zZThAx7sGRiZHHjUrpc_f1I9c-j_ehNDOTtrzrkQ3kDKZfJdUCgZJ0s2bufSQX91RKfHt_ZCzV8oeKySpIpx; ADRUM_BTa=R:0|g:a5bf79ed-1ca8-45d0-804d-d9f0490eb35a|n:ihsco_86f4fc53-86e8-4feb-bc7a-7921d526821f; ADRUM_BT1=R:0|i:461009; ADRUM_BTs=R:0|s:f",
}

# session data - cookies
# session_cookies = {
#     # these two cookies are the most important ones for the scraping
#     ".AspNet.ApplicationCookie": "tDpBsG1oYSJIc_3Vb2geMLwS1EdEi8CceoZsq8p3i27RVfqQFiGEIGdwA3P3e9BduhX90QmJLe40P6rBGrm8EpRF6qtq6URvSoMMrDFMp15mz6WkwNPqE2TKqm87ENzQ_rGgwnptOcAm03TcokUgajbG1KGGnyuZyiBwVRGlHRvkiWpH8N-Qq4SI8cmdwk6nobUx6oW80cFHL1A1duolWZxr9d9E-fNnQWO-LwzL3Oz4F8Sxn7uVujUUT91ELWvvWGtWLoz2i7By2jThKlznyl57hzo4spj-f9RirHprTmHoj5RetwBrEfYRpLw2Ukd8FQDG4Z6DdikeMNW-v_ZSAcHPc1YWaT7_lFTblwiUtL3n6AGhh2ygWNZOz_ZYDIxHFEJuUupOhol--GiVzVRLbK0mqptdSm2nmk9Rj-fcUn7Jgr0SOIvgkJCESu4U0U9AjPlJlmn3L79sRe5XT2V6ScA0f_8LjnMJalrl8HiQY4JIaCACvK0bJ_wFzrNlkOOeZRwcfi64TampIsqk6SC-n7Z9jq4sOEQcg8nO_V8q8qiFv_S0",    
#     "ASP.NET_SessionId": "vgw3qjc0jnenb2fzbeu0wzrc",

#     "BIGipServer~ProdWeb~pool-maritime.ihs.com-80": "rd1100o00000000000000000000ffff0aa8006bo80",
#     "LastBuilderVisited": "JPN138Miho Zosensho K.K.+RUS018Vyborgskiy Sudostroitelnyy Zavod%2c Oao",
#     "LastShipVisited": "1009340A+8009129DF 19+9237371WEC VERMEER+9237369MOVEON+9334600ABAI+7920259ABDUL B",
#     "ShipCommercialHistoryExpanded": "ShipCommercialHistoryExpanded",
#     "ckDefault": "page=shipsearch&records=20",
#     "ckShip": "db_name001=VESSELNAMEBROWSE&en_name001=Name of Ship&db_name002=DATEOFBUILDBROWSE&en_name002=Built&" \
#               "db_name003=DWT&en_name003=Deadweight&db_name004=FLAG&en_name004=Flag&db_name005=STATUSBROWSE&" \
#               "en_name005=Status&db_name006=OWNER&en_name006=Registered Owner&db_name007=NBPriceUSDEquivalent&" \
#               "en_name007=Newbuilding Price&db_name008=EngineBuilderLargest&en_name008=Engine Builder&" \
#               "db_name009=EngineMakeLargest&en_name009=Engine Design&db_name010=SHIPBUILDER&" \
#               "en_name010=Shipbuilder&db_name011=BUILDERCODE&en_name011=Shipbuilder Code&" \
#               "db_name012=YEAROFBUILDBROWSE&en_name012=Year",
#     "ckShipDiv": "hidehidehidehidehideshowhidehide",
#     "list": "",
#     "rememberMeLogin": "C85751F4D8BAC8E64E7C1278E492E3F616BC06CAD6FE828D8DD1CED1D48892E81320AE0853EE3F6B5BF" \
#                        "47B6B82CBA646A7CD8EA72472A24EDEFA6A78F14AABFA34F9C3001C95D0C472E89C263A6B2D1138EA70FF73" \
#                        "A2EA721BAE40B17B83539F14889F7FB612664A05B31FCD",
#     "shipsearch": "",
#     "shiphead": "1",
# }

print("Starting...")

# setup HTTP session
session = requests.Session()
session.headers.update(session_headers)
# session.cookies.update(session_cookies)
# session.max_redirects = 100

# some useful constants
LIMIT = 100000  # requests limit
TIMEOUT_DELAY_MAX = 4  # max timeout between requests, seconds
TIMEOUT_CADENCE = 100  # timeout cadence - # of requests between timeout/delay
IMO_NUMBERS_FILE = "EquasisToIACS_20220401_731.csv"  # csv file with imo numbers (warning - format!)
BASE_WORKING_DIR = os.getcwd() + "/.seaweb_db"
RAW_SHIPS_DIR = BASE_WORKING_DIR + "/seaweb"
MAIN_SHIP_DATA_FILE = "ship_main.html"

# debug output
print(f"OS working dir: [{os.getcwd()}]")
print(f"Base working dir: [{BASE_WORKING_DIR}].")
print(f"Ships dir: [{RAW_SHIPS_DIR}].")


def get_base_data(req_limit: int = LIMIT, req_delay: int = TIMEOUT_DELAY_MAX,
                  req_delay_cadence: int = TIMEOUT_CADENCE,
                  imo_numbers_file: str = IMO_NUMBERS_FILE, imo_numbers_file_delimeter: str = ";",
                  processed_imo_numbers: str = "processed.csv"):

    print("Working -> get_base_data().")

    # calculate full abs path to IMO numbers file
    file_imo_numbers_list = BASE_WORKING_DIR + "/" + imo_numbers_file
    print(f"Use IMO numbers file: {file_imo_numbers_list}")

    # calculate full abs path to <processed IMO numbers> file
    file_processed_imo_numbers = BASE_WORKING_DIR + "/" + processed_imo_numbers
    print(f"Use <processed IMO numbers file>: {file_processed_imo_numbers}")

    with open(file_imo_numbers_list) as csv_file:  # read CSV from equasis with IMO numbers
        csv_reader = csv.reader(csv_file, delimiter=imo_numbers_file_delimeter)

        line_count = 0
        for row in csv_reader:  # iterate over all IMO numbers
            print(f"Total processed: {line_count}")  # just a debug

            if line_count > req_limit:  # just a stopper
                break

            if line_count == 0:  # skip the header row
                print(f'Column names are {", ".join(row)}')
                line_count += 1
                with open(file_processed_imo_numbers, mode='w') as processed_file:  # rewrite existing file
                    processed_writer = csv.writer(processed_file, delimiter=',', quotechar='"',
                                                  quoting=csv.QUOTE_MINIMAL)
                    processed_writer.writerow([f"{row[0]}", "Processed"])

            else:  # data rows processing
                print(f'\nProcessing: IMO = {row[0]}, SHIP NAME = {row[1]}')
                line_count += 1

                ship_dir = RAW_SHIPS_DIR + "/" + row[0]  # directory to store the current ship
                print(f"\tship dir: {ship_dir}")

                with open(file_processed_imo_numbers, mode='a') as processed_file:  # other mode='w'
                    processed_writer = csv.writer(processed_file, delimiter=',', quotechar='"',
                                                  quoting=csv.QUOTE_MINIMAL)
                    processed_writer.writerow([f"{row[0]}", "+"])

                if Path(ship_dir).exists() and Path(ship_dir).is_dir():  # skip already processed ships
                    print(f"\tShip IMO: {row[0]} already processed. Skipped.")
                    continue

                # artificial delay for every 50 run
                if line_count % req_delay_cadence == 0:
                    delay_sec = random.randint(1, req_delay)  # delay 1 to X sec (both inclusive)
                    print(f"\tDelay {delay_sec} seconds.")
                    time.sleep(delay_sec)

                # real ship processing
                response = session.get(ship_url + row[0], allow_redirects=True)  # request the site...
                if response.status_code != 200:  # check that 200 is returned
                    print(f"Error code: {response.status_code} returned! Stopping!")
                    break

                os.makedirs(ship_dir, exist_ok=True)  # if all is OK - create dir for the ship data
                with open(Path(ship_dir + '/' + MAIN_SHIP_DATA_FILE), 'w') as f:  # write received content to file
                    f.write(response.text)
                    print(f"\tWritten file: {ship_dir + '/' + MAIN_SHIP_DATA_FILE}")

        print(f'Processed {line_count} lines.')


def get_extended_data(req_limit: int = LIMIT, req_delay: int = TIMEOUT_DELAY_MAX,
                      req_delay_cadence: int = TIMEOUT_CADENCE,
                      imo_numbers_file: str = IMO_NUMBERS_FILE, imo_numbers_file_delimeter: str = ";",
                      processed_imo_numbers: str = "processed_extended.csv"):

    print("Working -> get_extended_data().")

    # calculate full abs path to IMO numbers file
    file_imo_numbers_list = BASE_WORKING_DIR + "/" + imo_numbers_file
    print(f"Use IMO numbers file: {file_imo_numbers_list}")

    # calculate full abs path to <processed IMO numbers> file
    file_processed_imo_numbers = BASE_WORKING_DIR + "/" + processed_imo_numbers
    print(f"Use <processed IMO numbers file>: {file_processed_imo_numbers}")

    with open(file_imo_numbers_list) as csv_file:  # read CSV from equasis with IMO numbers
        csv_reader = csv.reader(csv_file, delimiter=imo_numbers_file_delimeter)

        line_count = 0
        for row in csv_reader:  # iterate over all IMO numbers
            print(f"Total processed: {line_count}")  # just a debug

            if line_count > req_limit:  # just a stopper
                break

            if line_count == 0:  # skip the header row
                print(f'Column names are {", ".join(row)}')
                line_count += 1

            # todo: remove file log for processed?
            #     with open(file_processed_imo_numbers, mode='w') as processed_file:  # rewrite existing file
            #         processed_writer = csv.writer(processed_file, delimiter=',', quotechar='"',
            #                                       quoting=csv.QUOTE_MINIMAL)
            #         processed_writer.writerow([f"{row[0]}", "Processed"])

            else:  # data rows processing
                print(f'\nProcessing: IMO = {row[0]}, SHIP NAME = {row[1]}')
                line_count += 1

                ship_dir = RAW_SHIPS_DIR + "/" + row[0]  # directory to store the current ship
                print(f"\tship dir: {ship_dir}")

                # check existence of several files with additional info and request it if missing
                skip_delay = True
                for key in ship_additional_data_urls:
                    # print(f"key={key}, value={ship_additional_data_urls[key]}")
                    ship_ext_file = ship_dir + "/" + key + ".html"
                    if not Path(ship_ext_file).exists():
                        # print(f"\tFile [{key}].html doesn't exist, downloading...")  # <- too much output
                        skip_delay = False  # we're doing real requests, so need a delay
                        # download missing file
                        response = session.get(ship_additional_data_urls[key] + row[0])
                        # check that 200 is returned - break otherwise
                        if response.status_code != 200:
                            print(f"Error code: {response.status_code} returned! Stopping!")
                            # break
                            return
                        # save downloaded file if 200 OK returned
                        with open(Path(ship_ext_file), 'w') as f:  # write received content to file
                            f.write(response.text)
                            print(f"\tWritten file: {ship_ext_file}")

                # todo: remove file log for processed?
                # # add the current IMO as processed
                # with open(file_processed_imo_numbers, mode='a') as processed_file:  # other mode='w'
                #     processed_writer = csv.writer(processed_file, delimiter=',', quotechar='"',
                #                                   quoting=csv.QUOTE_MINIMAL)
                #     processed_writer.writerow([f"{row[0]}", "+"])

                # artificial delay for every XX runs
                if not skip_delay and line_count % req_delay_cadence == 0:
                    delay_sec = random.randint(1, req_delay)  # delay 1 to X sec (both inclusive)
                    print(f"\tDelay {delay_sec} seconds.")
                    time.sleep(delay_sec)

        print(f'Processed {line_count} lines.')


def read_file(file_path: str):
    with open(file_path, mode='r') as infile:
        return infile.read()


def ship_main_parse(html_text: str):
    # todo: read from file - replace with the method parameter
    data_file = os.getcwd() + "/temp/9336505/ship_main.html"
    data = read_file(data_file)

    soup = BeautifulSoup(data, "html.parser")  # parser
    # find all data rows
    data_rows = soup.find_all("div", class_="col-sm-12 col-md-6 col-lg-6")

    for row in data_rows:
        # print(row)
        key: str = row.find("div", class_="col-4 keytext").text
        value: str = row.find("div", class_="col-8 valuetext").text
        print(f"{key} -> {value}")


def process_raw_data():
    ships_dirs = os.listdir(RAW_SHIPS_DIR)
    print(f"Total ships: {len(ships_dirs)}.")

    counter: int = 0
    # iterate over all dirs/ships and process data
    for ship in ships_dirs:

        if not ship.isnumeric():  # skip non-numeric dirs
            print(f"Found non-numeric object: [{ship}]")
            continue

        ship_data: str = read_file(RAW_SHIPS_DIR + "/" + ship + "/" + MAIN_SHIP_DATA_FILE)
        if "Access is denied." in ship_data:
            continue

        counter += 1

    print(f"Ships with data: {counter}")


@click.command()
@click.option('--imo-file', default=IMO_NUMBERS_FILE, help='File with IMO numbers.',
              type=str, show_default=True)
@click.option('--imo-file-delim', default=";", help='Default delimeter for file with IMO numbers.',
              type=str, show_default=True)
@click.option('--processed-base-file', default="processed.csv",
              help='Processed IMO numbers (base info).', type=str, show_default=True)
@click.option('--processed-ext-file', default="processed_extended.csv",
              help='Processed IMO numbers (ext info)', type=str, show_default=True)
def main(imo_file: str, imo_file_delim: str, processed_base_file: str, processed_ext_file: str):
    # get_base_data(imo_numbers_file=imo_file, imo_numbers_file_delimeter=imo_file_delim,
    #               processed_imo_numbers=processed_base_file)
    # get_extended_data(imo_numbers_file=imo_file, imo_numbers_file_delimeter=imo_file_delim,
    #                   processed_imo_numbers=processed_ext_file)

    # process_raw_data()
    ship_main_parse("")


if __name__ == '__main__':
    main()
