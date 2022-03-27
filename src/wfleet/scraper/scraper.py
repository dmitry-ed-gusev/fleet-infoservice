#!/usr/bin/env python3
# coding=utf-8

"""
    Main Fleet Scraper Module for all particular scrapers.

    Important notes:
      - scraper can be run in 'DRY RUN' mode - nothing will happen, only empty excel files
        will be created in cache (dry run directory will be marked with '-dryrun' postfix.
      - scraper can be run in 'requests number limited mode' - # todo: add description!

    Useful tech resources:
      - (remove dirs) https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
      - (click library) https://click.palletsprojects.com/en/8.0.x/

    Created:  Gusev Dmitrii, 10.01.2021
    Modified: Dmitrii Gusev, 27.03.2022
"""

# todo: create unit tests for dry run mode
# todo: create unit tests for request limited run
# todo: implement multithreading for calling scrapers, some of scrapers will spawn more threads (???)
# todo: add cmd key for list of scrapers

import os
import logging
import logging.config
import click
from wfleet.scraper import VERSION
from wfleet.scraper.config.scraper_config import CONFIG
from wfleet.scraper.config.logging_config import LOGGING_CONFIG
from wfleet.scraper.cache.scraper_cache import cache_cleanup
from wfleet.scraper.engine.scraper_engine import scrap_all_data

# some useful defaults - main scraper logger, application name
MAIN_LOGGER: str = "wfleet.scraper.scraper"
APP_NAME: str = "World Fleet Scraper"

# main module logger
log = logging.getLogger(MAIN_LOGGER)


@click.group()
@click.option('--dry-run', default=False, is_flag=True, help='Dry run mode for Scraper (no action).')
@click.version_option(version=VERSION, prog_name=APP_NAME)
@click.pass_context  # pass context to other sub command(s)
def main(context, dry_run: bool):
    """World Fleet Scraper. (C) Dmitrii Gusev, Sergei Lukin, 2020-2022."""

    # makes sure logging directories exists
    os.makedirs(CONFIG["cache_dir"] + "/logs/", exist_ok=True)
    # init logger with config dictionary
    logging.config.dictConfig(LOGGING_CONFIG)
    log.debug(f"Logging for {APP_NAME} is configured.")

    # log some initial info
    log.info(f"{APP_NAME} application init finished OK. Starting the application.")

    # initial debug info
    log.debug(f"Scraper working dir: {os.getcwd()}")
    log.debug(f"Scraper configuration: {CONFIG}")

    # dry run mode on - warning/debug message
    if dry_run:
        log.warning("DRY RUN MODE IS ON!")
    else:
        log.debug("Dry run mode is off.")

    # ensure that context.obj exists and is a dict (in case `main()` is called by means other than the
    # `if` block below, like integrated with setuptools - call from entry point)
    context.ensure_object(dict)
    # init the context
    context.obj['DRYRUN'] = dry_run


@main.command(help="Scraper local cache cleanup.")
@click.pass_context
def cleanup(context):
    log.debug("Executing command: cleanup.")
    click.echo(f"DRYRUN is {'on' if context.obj['DRYRUN'] else 'off'}")
    cache_cleanup(context.obj['DRYRUN'])


@main.command(help="Perform data scraping from all sources.")
@click.option('--req-count', default=0, help='Limit number of requests for parsers, 0 - no limit.',
              type=int, show_default=True)
@click.pass_context
def scrap(context, req_count: int):
    log.debug("Executing command: scrap.")
    log.debug(f"Scraper requests limit: {req_count}")
    scrap_all_data(context.obj['DRYRUN'], req_count)


if __name__ == '__main__':
    main(obj={})
