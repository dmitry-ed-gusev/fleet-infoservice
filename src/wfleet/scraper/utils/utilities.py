# coding=utf-8

"""
    Common utilities module for Fleet DB Scraper.
    Useful materials:
      - (datetime) https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

    Created:  Gusev Dmitrii, 26.04.2021
    Modified: Gusev Dmitrii, 30.05.2021
"""

import logging
import hashlib

from . import constants as const
from datetime import datetime

# init module logger
log = logging.getLogger(const.LOGGING_UTILITIES_LOGGER)

# useful module constants
RUS_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ENG_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUM_CHARS = "0123456789"
SPEC_CHARS = "-"


def get_hash_bucket_number(value: str, buckets: int) -> int:
    """Generate hash bucket number for the given value, generated bucket number
    will be less than provided buckets count.
    :param value:
    :param buckets:
    :return:
    """
    log.debug(f"get_hash_bucket_number(): value [{value}], buckets [{buckets}].")

    if value is None or len(value.strip()) == 0:  # fail-fast if value is empty
        raise ValueError("Provided empty value!")

    if buckets <= 0:  # if buckets number <= 0 - generated bucket number is always 0
        log.debug(f"get_hash_bucket_number(): buckets number [{buckets}] <= 0, return 0!")
        return 0

    # value is OK and buckets number is > 0
    hex_hash = hashlib.md5(value.encode("utf-8")).hexdigest()  # generate hexadecimal hash
    int_hash = int(hex_hash, 16)  # convert it to int (decimal)
    bucket_number = int_hash % buckets  # define bucket number as division remainder
    log.debug(
        f"get_hash_bucket_number(): hash: [{hex_hash}], decimal hash: [{int_hash}], "
        f"generated bucket: [{bucket_number}]."
    )

    return bucket_number


def add_value_to_hashmap(hashmap: dict, value: str, buckets: int) -> dict:
    """Add value to the provided hash map with provided total buckets number.
    :param hashmap:
    :param value:
    :param buckets:
    """
    log.debug(f"add_value_to_hashmap(): hashmap [{hashmap}], value [{value}], buckets [{buckets}].")

    if hashmap is None or not isinstance(hashmap, dict):  # fail-fast - hash map type check
        raise ValueError(f"Provided empty hashmap [{hashmap}] or it isn't dictionary!")
    if value is None or len(value.strip()) == 0:  # fail-fast - empty/zero-length value
        raise ValueError(f"Provided empty value [{value}]!")

    bucket_number = get_hash_bucket_number(value, buckets)  # bucket number for the value
    if hashmap.get(bucket_number) is None:  # bucket is not initialized yet
        hashmap[bucket_number] = list()
    hashmap.get(bucket_number).append(value)  # add value to the bucket

    return hashmap


def build_variations_hashmap(buckets: int = 0) -> dict:
    """Build hashmap of all possible variations of symbols for further search.
    :param buckets: number of buckets to divide symbols
    :return: list of variations
    """
    log.debug(f"build_variations_hashmap(): buckets [{buckets}].")

    result = dict()  # resulting dictionary

    for letter1 in RUS_CHARS + ENG_CHARS + NUM_CHARS:
        for letter2 in RUS_CHARS + ENG_CHARS + NUM_CHARS:
            result = add_value_to_hashmap(result, letter1 + letter2, buckets)  # add value to hashmap

            for spec_symbol in SPEC_CHARS:
                result = add_value_to_hashmap(
                    result, letter1 + spec_symbol + letter2, buckets
                )  # add value to hashmap

    return result


def build_variations_list() -> list:
    """Build list of possible variations of symbols for search.
    :return: list of variations
    """
    log.debug("build_variations_list(): processing.")

    result = list()  # resulting list

    for letter1 in RUS_CHARS + ENG_CHARS + NUM_CHARS:
        for letter2 in RUS_CHARS + ENG_CHARS + NUM_CHARS:
            result.append(letter1 + letter2)  # add value to resulting list

            for spec_symbol in SPEC_CHARS:
                result.append(letter1 + spec_symbol + letter2)  # add value to resulting list

    return result


def generate_timed_filename(postfix: str) -> str:
    """Generates file name with timestamp and provided postfix, human-readable.
    :param postfix:
    :return:
    """
    log.debug(f"generate_timed_filename(): generating file name with postfix {postfix}.")

    result: str = datetime.now().strftime(const.SCRAPER_CACHE_DIRECTORY_TIMESTAMP_PATTERN)
    if postfix is not None and len(postfix.strip()) > 0:
        result += "-" + postfix.strip()

    return result


# todo: implement unit tests that module isn't runnable directly!
if __name__ == "__main__":
    print("Don't run this utility script directly!")