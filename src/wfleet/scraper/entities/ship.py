#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Ships related DTOs for data scraping.
    Currently supports:
      - BaseShipDto - class contains basic ship info alongside with some necessary tech info
      - ExtendedShipDto - class contains extended ship info

    Created:  Gusev Dmitrii, 10.01.2021
    Modified: Dmitrii Gusev, 09.06.2022
"""

# todo: implement creation of dataclass from dictionary, see the link below
# todo: https://www.reddit.com/r/learnpython/comments/9h74no/convert_dict_to_dataclass/

from datetime import datetime
from dataclasses import dataclass
from dataclasses import asdict, astuple, field
from wfleet.scraper.config.scraper_config import Config


@dataclass
class ShipDto:
    """Ship DTO object - ship with base attributes, used for all scrapers."""

    # ship's identity data (composite ID)
    imo_number: str           # (ID) imo number of the ship
    proprietary_number1: str  # (ID) proprietary number #1 (reg/riv-reg/etc number)
    proprietary_number2: str  # (ID) proprietary number #2 (reg/riv-reg/etc number)
    source_system: str        # (ID) source system name where ship data was retrieved

    # timestamp for the ship entity (field is excluded from comparison)
    timestamp: datetime = field(compare=False)

    # full ship's data
    flag: str = ""             # ship's flag
    main_name: str = ""        # ship's main name
    secondary_name: str = ""   # ship's secondary name
    gross: str = ""            # gross (валовая вместимость)
    deadweight: str = ""       # deadweight (дедвейт)
    home_port: str = ""        # ship's home port
    call_sign: str = ""        # ship's call sign
    project: str = ""          # ship's project number
    owner: str = ""            # ship's owner
    owner_address: str = ""    # ship owner's address
    owner_ogrn: str = ""       # ship owner's ОГРН number
    owner_ogrn_date: str = ""  # ship owner's ОГРН date
    mmsi_number: str = ""      # MMSI No
    build_number: str = ""     # ship's build number
    ship_type: str = ""        # ship's type
    build_date: str = ""       # ship's build date
    build_place: str = ""      # ship's build place
    status: str = ""           # ship's current status
    ship_operator: str = ""            #
    ship_operator_address: str = ""    #
    ship_operator_seaweb_id: str = ""  #
    ship_builder: str = ""             #
    ship_builder_seaweb_id: str = ""   #

    # some tech info
    extended_info_url: str = ""               # URL for ship extended info (usually - separated page)
    init_datetime: datetime = datetime.now()  # timestamp of creating ship instance

    @classmethod
    def ship_from_dict(cls, ship_dict: dict[str, str]):

        if not ship_dict:
            raise ValueError("Provided empty dictionary for building a ShipDto instance!")

        config = Config()  # get system config instance

        # base parameters for the constructor
        imo_number: str = ship_dict['imo_number']
        number1: str = "-"
        number2: str = "-"
        source_system: str = ship_dict['source_system']
        timestamp: datetime = datetime.strptime(ship_dict['timestamp'], config.timestamp_pattern)
        # construct the instance of ShipDto dataclass
        ship = cls(imo_number, number1, number2, source_system, timestamp)

        # additional data for the ship
        ship.main_name = ship_dict['ship_name']
        ship.ship_type = ship_dict['ship_type']
        ship.gross = ship_dict['gross']
        ship.deadweight = ship_dict['deadweight']
        ship.call_sign = ship_dict['call_sign']
        ship.mmsi_number = ship_dict['mmsi_no']
        ship.build_date = ship_dict['build_year']
        ship.flag = ship_dict['flag']
        ship.status = ship_dict['status']
        ship.ship_operator = ship_dict['ship_operator']
        ship.ship_operator_address = ship_dict['ship_operator_address']
        ship.ship_operator_seaweb_id = ship_dict['ship_operator_seaweb_id']
        ship.ship_builder = ship_dict['ship_builder']
        ship.ship_builder_seaweb_id = ship_dict['ship_builder_seaweb_id']

        return ship


if __name__ == '__main__':
    ship1 = ShipDto('999', '123', '', 'system', datetime.now())
    print(ship1)
    print(asdict(ship1))
    print(astuple(ship1))
