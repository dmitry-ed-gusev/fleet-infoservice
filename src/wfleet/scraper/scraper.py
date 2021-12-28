#!/usr/bin/env python3
# coding=utf-8

"""
    Main Fleet Scraper Module for all particular scrapers.

    Important notes:
      - scraper can be run in 'DRY RUN' mode - nothing will happen, only empty excel files
        will be created in cache (dry run directory will be marked with '-dryrun' postfix.
      - scraper can be run in 'requests number limited mode' - # todo: add description!

    Useful resources:
      - (remove dirs) https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
      - (click library) https://click.palletsprojects.com/en/8.0.x/

    Created:  Gusev Dmitrii, 10.01.2021
    Modified: Dmitrii Gusev, 28.12.2021
"""

# todo: create unit tests for dry run mode
# todo: create unit tests for request limited run
# todo: implement multithreading for calling scrapers, some of scrapers will spawn more threads (???)

import os
import logging
import logging.config
import click
from wfleet.scraper import VERSION
from wfleet.scraper.config.scraper_config import CONFIG
from wfleet.scraper.config.logging_config import LOGGING_CONFIG
from wfleet.scraper.engine.scraper_engine import cache_cleanup, scrap_all_data

# some useful defaults - main scraper logger, application name
MAIN_LOGGER: str = "wfleet.scraper"
APP_NAME: str = "World Fleet Scraper"

log = logging.getLogger(MAIN_LOGGER)  # main module logger


@click.group()
@click.option('--dry-run', default=False, is_flag=True, help='Dry run for Scraper (no action).')
# todo: add option for the # of requests for scraper
# @click.option('--zzz', default=False, is_flag=True, help='ZZZ.')
@click.version_option(version=VERSION, prog_name=APP_NAME)
@click.pass_context  # pass context to other sub command(s)
def main(context, dry_run: bool):
    """World Fleet Scraper. (C) Dmitrii Gusev, Sergei Lukin, 2020-2022."""

    # makes sure logging directories exists
    os.makedirs(CONFIG["cache_dir"] + "/logs/", exist_ok=True)
    # init logger with config dictionary
    logging.config.dictConfig(LOGGING_CONFIG)

    # log some initial info
    log.info(f"{APP_NAME} application init finished OK. Starting the application.")
    # initial debug info
    log.debug(f"Logging for module {MAIN_LOGGER} is configured.")
    log.debug(f"Scraper working dir: {os.getcwd()}")
    log.debug(f"Scraper configuration: {CONFIG}")
    # dry run mode on - warning/debug message
    if dry_run:
        log.warning("DRY RUN MODE IS ON!")
    else:
        log.info("Dry run mode is off.")

    # ensure that context.obj exists and is a dict (in case `main()` is called by means other than the
    # `if` block below, like integrated with setuptools - call from entry point)
    context.ensure_object(dict)
    # init the context
    context.obj['DRYRUN'] = dry_run


@main.command(help="Scraper cache cleanup.")
@click.pass_context
def cleanup(context):
    log.debug("Executing command: cleanup.")
    click.echo(f"DRYRUN is {'on' if context.obj['DRYRUN'] else 'off'}")
    cache_cleanup(context.obj['DRYRUN'])


@main.command(help="Perform data scraping.")
@click.pass_context
def scrap(context):
    log.debug("Executing command: scrap.")
    click.echo(f"DRYRUN is {'on' if context.obj['DRYRUN'] else 'off'}")
    scrap_all_data(context.obj['DRYRUN'])


if __name__ == '__main__':
    main(obj={})
