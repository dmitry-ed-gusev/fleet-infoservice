# coding=utf-8

"""
    Ships related DTOs for data scraping.
    Currently supports:
      - BaseShipDto - class contains basic ship info alongside with some necessary tech info
      - ExtendedShipDto - class contains extended ship info

    Created:  Gusev Dmitrii, 10.01.2021
    Modified: Dmitrii Gusev, 15.04.2022
"""

from dataclasses import dataclass
from dataclasses import asdict, astuple
from datetime import datetime


@dataclass
class ShipDto:
    """Ship DTO object - ship with base attributes, used for all scrapers."""

    # ship's identity data (composite ID)
    imo_number: str           # (ID) imo number of the ship
    proprietary_number1: str  # (ID) proprietary number #1 (reg/riv-reg/etc number)
    proprietary_number2: str  # (ID) proprietary number #2 (reg/riv-reg/etc number)
    source_system: str        # (ID) source system where ship data was retrieved
    timestamp: datetime       # timestamp for the ship entity

    # main ship's data
    flag: str = ""             # ship's flag
    main_name: str = ""        # ship's main name
    secondary_name: str = ""   # ship's secondary name
    home_port: str = ""        # ship's home port
    call_sign: str = ""        # ship's call sign
    project: str = ""          # ship's project number
    owner: str = ""            # ship's owner
    owner_address: str = ""    # ship owner's address
    owner_ogrn: str = ""       # ship owner's ОГРН number
    owner_ogrn_date: str = ""  # ship owner's ОГРН date

    # additional ship's data
    build_number: str = ""  # ship's build number
    ship_type: str = ""  # ship's type
    build_date: str = ""  # ship's build date
    build_place: str = ""  # ship's build place

    # some tech info
    extended_info_url: str = ""  # URL for ship extended info (usually - separated page)
    init_datetime: datetime = datetime.now()  # timestamp of creating ship instance

    # def __init_sss__(self, imo_number: str, proprietary_number1: str, proprietary_number2: str,
    #              source_system: str, timestamp: datetime):
    #     """
    #     :param imo_number:
    #     :param proprietary_number1:
    #     :param proprietary_number2:
    #     :param source_system:
    #     :param timestamp:
    #     """
    #     self.imo_number = imo_number  # (ID) imo number of the ship
    #     self.proprietary_number1: str = (
    #         proprietary_number1  # (ID) proprietary number #1 (reg/riv-reg/etc number)
    #     )
    #     self.proprietary_number2: str = (
    #         proprietary_number2  # (ID) proprietary number #2 (reg/riv-reg/etc number)
    #     )
    #     self.source_system: str = source_system  # (ID) source system where ship data was retrieved


if __name__ == '__main__':
    ship1 = ShipDto('999', '123', '', 'system', datetime.now())
    print(ship1)
    ship1.sss = 'sss'
    print(ship1)
    print(asdict(ship1))
    print(astuple(ship1))
