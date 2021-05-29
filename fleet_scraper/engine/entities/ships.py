# coding=utf-8

"""
    Ships related entities for scraping.

    Created:  Gusev Dmitrii, 10.01.2021
    Modified: Dmitrii Gusev, 28.05.2021
"""


# todo: implement unit tests for this module / script

class BaseShipDto:
    """Base ship DTO object - ship with base attributes, used for all scrapers."""

    # def __new__(cls, *args, **kwargs):  # creates new instance, called before __init()__
    #     pass

    def __init__(self, imo_number: str):  # inits newly created (by __new()__) object instance
        self.imo_number = imo_number
        self.proprietary_number = ''
        self.source_code = ''
        self.flag = ''
        self.main_name = ''
        self.secondary_name = ''
        self.home_port = ''
        self.call_sign = ''

    def __str__(self) -> str:  # magic method for object string representation - str(object)
        return f"IMO #: {self.imo_number}, proprietary #: {self.reg_number}, flag: {self.flag}, " \
               f"name: {self.main_name}, secondary name: {self.secondary_name}, " \
               f"port: {self.home_port}, call: {self.call_sign}"

    # def __repr__(self):
    #     # todo: implement function!
    #     raise NotImplemented("Not implemented yet!")
    #
    # # def __eq__(self, other):  # equals magic method (==)
    #     # todo: implement function!
    #     raise NotImplemented("Not implemented yet!")
    #
    # def __ne__(self, other):  # not equals magic method (!=)
    #     # todo: implement function!
    #     raise NotImplemented("Not implemented yet!")
    #
    # def __hash__(self) -> int:  # hash magic method hash()
    #     # todo: implement function!
    #     raise NotImplemented("Not implemented yet!")


class ExtendedShipDto(object):
    """Extended ship DTO object - ship with extended attributes, used for all scrapers."""

    def __init__(self, imo_number: str):
        self.imo_number = imo_number
