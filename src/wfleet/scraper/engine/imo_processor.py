#!/usr/bin/env python3
# coding=utf-8

"""
    IMO numbers list processor - load, update, etc.

    Created:  Gusev Dmitrii, 18.04.2022
    Modified:
"""

import csv
import logging
import shutil
from typing import Set
from wfleet.scraper.config.scraper_config import CONFIG
from wfleet.scraper.config.scraper_config import MSG_MODULE_ISNT_RUNNABLE

log = logging.getLogger(__name__)
log.debug(f"Logging for module {__name__} is configured.")


def reset_imo_numbers() -> None:
    file: str = CONFIG['imo_file']
    backup_file = CONFIG['imo_file_backup']

    shutil.copy(file, backup_file)  # create a backup copy of the file

    imo_numbers: Set[int] = set()
    with open(file, mode='r') as imo_file:  # read CSV with IMO numbers
        csv_reader = csv.reader(imo_file, delimiter=';')

        header_row = False
        for row in csv_reader:  # process all rows in a file

            if not header_row:  # skip the header row
                header_row = True
                continue

            try:  # add imo number to set
                imo_numbers.add(int(row[0]))
            except ValueError:  # skip on error
                log.warning(f"Skipped non-numeric value: [{row[0]}]!")

    with open(file, mode='w') as imo_file:  # update imo numbers file
        csv_writer = csv.writer(imo_file, delimiter=';', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['IMO Number', 'Status'])  # write header row

        for imo in sorted(imo_numbers):  # write imo numbers back to file
            csv_writer.writerow([imo, '+'])


def is_imo_in_list(imo: str) -> None:
    pass


def add_imo_to_list(imo: str) -> None:
    pass


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
