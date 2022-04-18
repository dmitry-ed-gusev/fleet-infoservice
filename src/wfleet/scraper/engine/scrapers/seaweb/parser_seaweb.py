#!/usr/bin/env python3
# coding=utf-8

"""
    Data parser for Sea Web database. 
    Main data source address is https://maritime.ihs.com

    Created:  Gusev Dmitrii, 17.04.2022
    Modified: Gusev Dmitrii, 18.04.2022
"""

from typing import Dict, AnyStr
from bs4 import BeautifulSoup
from wfleet.scraper.entities.ship import ShipDto
from wfleet.scraper.config.scraper_config import MSG_MODULE_ISNT_RUNNABLE
from wfleet.scraper.exceptions.scraper_exceptions import ScraperException
from wfleet.scraper.utils.utilities import get_last_part_of_the_url


def _parse_ship_main(html_text: str) -> Dict[AnyStr, AnyStr]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException("Empty HTML text for parsing!")

    soup = BeautifulSoup(html_text, "html.parser")  # parser
    data_rows = soup.find_all("div", class_="col-sm-12 col-md-6 col-lg-6")  # find all data rows

    ship_data: dict = dict()
    for row in data_rows:  # iterate over data rows and parse data
        # print(f"\n{row}")  # <- debug output
        key: str = row.find("div", class_="col-4 keytext").text  # row -> key column
        value: str = row.find("div", class_="col-8 valuetext").text  # row -> value column
        anchor = row.find('a')  # anchor with the data for some of rows
        print(f"Data row: {key} -> {value}")  # <- debug output

        if key == 'Ship Name':
            ship_data['ship_name'] = value
        elif key == 'Shiptype':
            ship_data['ship_type'] = value
        elif key == 'IMO/LR No.':
            ship_data['imo_number'] = value
        elif key == 'Gross':  # валовая вместимость
            ship_data['gross'] = value
        elif key == 'Call Sign':
            ship_data['call_sign'] = value
        elif key == 'Deadweight':  # дедвейт
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


def _parse_ship_xxx1(html_text: str) -> Dict[AnyStr, AnyStr]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException("Empty HTML text for parsing!")


def _parse_ship_xxx2(html_text: str) -> Dict[AnyStr, AnyStr]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException("Empty HTML text for parsing!")


def _parse_ship_xxx3(html_text: str) -> Dict[AnyStr, AnyStr]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException("Empty HTML text for parsing!")


def _parse_ship_xxx4(html_text: str) -> Dict[AnyStr, AnyStr]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException("Empty HTML text for parsing!")


def _parse_ship_xxx5(html_text: str) -> Dict[AnyStr, AnyStr]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException("Empty HTML text for parsing!")


def _parse_ship_xxx6(html_text: str) -> Dict[AnyStr, AnyStr]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException("Empty HTML text for parsing!")


def _parse_ship_xxx7(html_text: str) -> Dict[AnyStr, AnyStr]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException("Empty HTML text for parsing!")


def _parse_ship_xxx8(html_text: str) -> Dict[AnyStr, AnyStr]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException("Empty HTML text for parsing!")


def _parse_ship_xxx1(html_text: str) -> Dict[AnyStr, AnyStr]:
    if not html_text:  # fail-fast behaviour
        raise ScraperException("Empty HTML text for parsing!")


def parse_ship(ship_dir: str) -> ShipDto:
    if not html_text:  # fail-fast behaviour
        raise ScraperException("Empty HTML text for parsing!")


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
