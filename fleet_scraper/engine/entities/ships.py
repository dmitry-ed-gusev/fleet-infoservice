# coding=utf-8

"""
    Ships related DTOs for data scraping.
    Currently supports:
      - BaseShipDto - class contains basic ship info alongside with some necessary tech info
      - ExtendedShipDto - class contains extended ship info

    Created:  Gusev Dmitrii, 10.01.2021
    Modified: Dmitrii Gusev, 13.06.2021
"""

from datetime import datetime

# todo: implement unit tests for this module / script


class BaseShipDto:
    """Base ship DTO object - ship with base attributes, used for all scrapers."""

    def __init__(self, imo_number: str, proprietary_number1: str, proprietary_number2: str, source_system: str):
        """
        :param imo_number:
        :param proprietary_number1:
        :param proprietary_number2:
        :param source_system:
        """
        # ship identity data
        self.imo_number: str = imo_number                    # (ID) imo number of the ship
        self.proprietary_number1: str = proprietary_number1  # (ID) proprietary number #1 (reg/riv-reg/etc number)
        self.proprietary_number2: str = proprietary_number2  # (ID) proprietary number #2 (reg/riv-reg/etc number)
        self.source_system: str = source_system              # (ID) source system where ship data was retrieved

        # main ship value
        self.flag: str = ''                                # ship's flag
        self.main_name: str = ''                           # ship's main name
        self.secondary_name: str = ''                      # ship's secondary name
        self.home_port: str = ''                           # ship's home port
        self.call_sign: str = ''                           # ship's call sign
        self.project: str = ''                             # ship's project number

        # additional tech info
        self.extended_info_url: str = ''                   # URL for ship extended info (usually - separated page)
        self.init_datetime: datetime = datetime.now()      # timestamp of creating ship instance

    def __str__(self) -> str:  # magic method for object string representation - str(object)
        """
        :return:
        """
        return f"IMO #: {self.imo_number}, proprietary #: {self.proprietary_number}, " \
               f"source system: {self.source_system}, flag: {self.flag}, " \
               f"main name: {self.main_name}, secondary name: {self.secondary_name}, " \
               f"home port: {self.home_port}, call sign: {self.call_sign}, " \
               f"timestamp: {self.init_datetime}, extended URL: {self.extended_info_url}"

    def hash_of_ship_value(self) -> int:
        """
        :return:
        """
        pass


class ExtendedShipDto(object):
    """Extended ship DTO object - ship with extended attributes, used for all scrapers."""

    def __init__(self, imo_number: str):
        self.imo_number = imo_number
