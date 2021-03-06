#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Data parser for Sea Web database.
    Main data source address is https://maritime.ihs.com

    Created:  Gusev Dmitrii, 17.04.2022
    Modified: Gusev Dmitrii, 29.05.2022
"""

import os
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

from wfleet.scraper.entities.ship import ShipDto
from wfleet.scraper.config.scraper_config import Config
from wfleet.scraper.config.scraper_messages import MSG_MODULE_ISNT_RUNNABLE, MSG_NOT_IMPLEMENTED
from wfleet.scraper.exceptions.scraper_exceptions import ScraperException
from wfleet.scraper.utils.utilities import get_last_part_of_the_url, read_file_as_text

EMPTY_HTML_MSG: str = "Empty HTML text for parsing!"

log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")

config = Config()  # get config instance


def _parse_ship_main(html_text: str, interest_keys: set[str] = set()) -> dict[str, str]:

    if not html_text:  # fail-fast behaviour
        raise ScraperException(EMPTY_HTML_MSG)

    soup = BeautifulSoup(html_text, "html.parser")  # parser
    data_rows = soup.find_all("div", class_="col-sm-12 col-md-6 col-lg-6")  # find all data rows

    ship_data: dict[str, str] = dict()  # resulting dictionary
    # current timestamp to string
    ship_data['timestamp'] = datetime.now().strftime(config.timestamp_pattern)
    # source system
    ship_data['source_system'] = 'seaweb'

    for row in data_rows:  # iterate over data rows and parse data
        # print(f"\n{row}")  # <- debug output
        key: str = row.find("div", class_="col-4 keytext").text  # row -> key column

        # if we specified interesting keys and the current key is not there - skip the rest!
        if interest_keys and key not in interest_keys:
            continue

        # row value may not be presented, if so - skip the rest
        row_value = row.find("div", class_="col-8 valuetext")
        if not row_value:
            log.debug('First attempt to get row value failed, trying different...')
            row_value = row.find("div", class_="col-8 valuetext alert_red")
            if not row_value:
                log.warn(f'Skipped row value for key: {key}!')
                continue

        value: str = row_value.text  # row -> value column
        anchor = row.find('a')  # anchor with the data for some of rows
        # print(f"Data row: {key} -> {value}")  # todo: debug output -> comment it!

        # todo: replace this construction with the dictionary (see 'case' operator for python)
        if key == 'Ship Name':
            ship_data['ship_name'] = value
        elif key == 'Shiptype':
            ship_data['ship_type'] = value
        elif key == 'IMO/LR No.':
            ship_data['imo_number'] = value
        elif key == 'Gross':  # ?????????????? ??????????????????????
            ship_data['gross'] = value
        elif key == 'Call Sign':
            ship_data['call_sign'] = value
        elif key == 'Deadweight':  # ??????????????
            ship_data['deadweight'] = value
        elif key == 'MMSI No.':
            ship_data['mmsi_no'] = value
        elif key == 'Year of Build':
            ship_data['build_year'] = value
        elif key == 'Flag':
            ship_data['flag'] = value
        elif key == 'Status':
            ship_data['status'] = value
        elif key == 'Operator':
            ship_data['ship_operator'] = value
            if anchor is not None:  # additional data for ship operator
                ship_data['ship_operator_seaweb_id'] = get_last_part_of_the_url(anchor.get('href'))
                ship_data['ship_operator_address'] = anchor.get('title')
            else:
                ship_data['ship_operator_seaweb_id'] = '-'
                ship_data['ship_operator_address'] = '-'
        elif key == 'Shipbuilder':
            ship_data['ship_builder'] = value
            if anchor is not None:  # additional data for ship builder
                ship_data['ship_builder_seaweb_id'] = get_last_part_of_the_url(anchor.get('href'))
            else:
                ship_data['ship_builder_seaweb_id'] = '-'
        else:
            raise KeyError(f"Unknown data key: {key}")

    return ship_data


def _parse_ship_xxx1(html_text: str) -> dict[str, str]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException(EMPTY_HTML_MSG)
    raise NotImplementedError(MSG_NOT_IMPLEMENTED)


def _parse_ship_xxx2(html_text: str) -> dict[str, str]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException(EMPTY_HTML_MSG)
    raise NotImplementedError(MSG_NOT_IMPLEMENTED)


def _parse_ship_xxx3(html_text: str) -> dict[str, str]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException(EMPTY_HTML_MSG)
    raise NotImplementedError(MSG_NOT_IMPLEMENTED)


def _parse_ship_xxx4(html_text: str) -> dict[str, str]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException(EMPTY_HTML_MSG)
    raise NotImplementedError(MSG_NOT_IMPLEMENTED)


def _parse_ship_xxx5(html_text: str) -> dict[str, str]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException(EMPTY_HTML_MSG)
    raise NotImplementedError(MSG_NOT_IMPLEMENTED)


def _parse_ship_xxx6(html_text: str) -> dict[str, str]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException(EMPTY_HTML_MSG)
    raise NotImplementedError(MSG_NOT_IMPLEMENTED)


def _parse_ship_xxx7(html_text: str) -> dict[str, str]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException(EMPTY_HTML_MSG)
    raise NotImplementedError(MSG_NOT_IMPLEMENTED)


def _parse_ship_xxx8(html_text: str) -> dict[str, str]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException(EMPTY_HTML_MSG)
    raise NotImplementedError(MSG_NOT_IMPLEMENTED)


def _parse_ship_xxx9(html_text: str) -> dict[str, str]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException(EMPTY_HTML_MSG)
    raise NotImplementedError(MSG_NOT_IMPLEMENTED)


def parse_one_ship(ship_dir: str) -> ShipDto:
    log.debug(f"parse_one_ship(): parsing ship [{ship_dir}].")

    # read and parse main ship data
    text: str = read_file_as_text(ship_dir + "/" + config.main_ship_data_file)
    ship_dict = _parse_ship_main(text)

    # read XXX data
    # todo: implement!

    # build Ship object from dictionary
    ship = ShipDto.ship_from_dict(ship_dict)
    log.debug(ship)

    return ship


def parse_all_ships(raw_ships_dir: str) -> list[ShipDto]:
    log.debug(f"parse_all_ships(): parsing ships in [{raw_ships_dir}].")

    if raw_ships_dir is None:  # fail-fast - empty dir
        raise ValueError("Provided empty ships dir!")

    # fail-fast - dir doesn't exist or not a dir
    if not Path(raw_ships_dir).exists() or not Path(raw_ships_dir).is_dir():
        raise ValueError(f"Provided ships dir [{raw_ships_dir}] doesn't exist or not a dir!")

    ships_dirs = os.listdir(raw_ships_dir)
    log.debug(f"Found total ships/directories: {len(ships_dirs)}.")

    ships_list: list[ShipDto] = list()
    for ship in ships_dirs:  # iterate over all dirs/ships and process data

        if not ship.isnumeric():  # skip non-numeric dirs
            log.warning(f"Found non-numeric object: [{ship}]")
            continue

        ship_dir: str = raw_ships_dir + "/" + ship

        # check - if we can parse this ship
        ship_data: str = read_file_as_text(ship_dir + "/" + config.main_ship_data_file)
        if "Access is denied." in ship_data:
            log.warning(f"Skipped current number [{ship}].")
            continue

        ships_list.append(parse_one_ship(ship_dir))

    return ships_list


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
