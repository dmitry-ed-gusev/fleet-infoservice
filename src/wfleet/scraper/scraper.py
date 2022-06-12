#!/usr/bin/env python3
# coding=utf-8

"""
    Main Fleet Scraper Module for all particular scrapers.

    Important notes:
      - scraper can be run in 'DRY RUN' mode - nothing will happen, only empty excel files
        will be created in cache (dry run directory will be marked with '-dryrun' postfix.
      - scraper can be run in 'requests number limited mode' - limited # of source web site requests

    Useful tech resources:
      - (remove dirs) https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
      - (click library) https://click.palletsprojects.com/en/8.0.x/

    Created:  Gusev Dmitrii, 10.01.2021
    Modified: Dmitrii Gusev, 04.05.2022
"""

# todo: create unit tests for dry run mode
# todo: create unit tests for request limited run
# todo: implement multithreading for calling scrapers, some of scrapers will spawn more threads (???)

import sys
import click
import logging
import logging.config
from wfleet.scraper import VERSION
from wfleet.scraper.config.scraper_config import Config
from wfleet.scraper.config.logging_config import LOGGING_CONFIG
from wfleet.scraper.cache.scraper_cache import cache_cleanup
from wfleet.scraper.engine.scraper_engine import scrap_all_data, execute_seaweb_parse, execute_seaweb_scrap

# context object keys
CONTEXT_DRYRUN: str = 'DRYRUN'

# general module init
log = logging.getLogger("wfleet.scraper")  # main module logger
config = Config()  # get config instance


@click.group()
@click.option('--dry-run', default=False, is_flag=True, help='Dry run mode for Scraper (no action).')
@click.version_option(version=VERSION, prog_name=config.app_name)
@click.pass_context  # pass context to other sub command(s)
def main(context, dry_run: bool):
    """World Fleet Scraper. (C) Dmitrii Gusev, Sergei Lukin, 2020-2022."""

    options = [opt for opt in sys.argv[1:] if opt.startswith('--')]  # collect cmd line arguments

    if "--help" not in options:  # if option --help is in the options list - do nothing
        # init logger with config dictionary + do initial debug output
        logging.config.dictConfig(LOGGING_CONFIG)
        log.debug(f"Logging for {config.app_name} configured. Configuration:\n{config}")
        log.info(f"{config.app_name} init finished OK. Starting the application.")

        # dry run mode on - warning/debug message
        if dry_run:
            log.warning("DRY RUN MODE IS ON!")
        else:
            log.debug("Dry run mode is off.")

        # ensure that context.obj exists and is a dict (in case `main()` is called by means other than the
        # `if` block below, like integrated with setuptools - call from entry point)
        context.ensure_object(dict)
        # init the context
        context.obj[CONTEXT_DRYRUN] = dry_run


@main.command(help="Scraper :: local scraper cache cleanup.")
@click.pass_context
def cleanup(context):
    log.debug("Executing command: cleanup.")
    # click.echo(f"DRYRUN is {'on' if context.obj[CONTEXT_DRYRUN] else 'off'}")
    cache_cleanup(context.obj[CONTEXT_DRYRUN])


@main.command(help="Scraper :: perform data scraping from sources.")
@click.option('--req-count', default=0, help='Limit number of requests for parsers, 0 - no limit.',
              type=int, show_default=True)
@click.pass_context
def scrap(context, req_count: int):
    log.debug(f"Executing command: scrap. Requests limit: {req_count}."
              f"Dry run: {context.obj[CONTEXT_DRYRUN]}.")
    scrap_all_data(context.obj[CONTEXT_DRYRUN], req_count)


@main.command(help="Scraper :: run Seaweb scraper engine.")
# @click.option()
@click.pass_context
def seaweb_scrap(context):
    log.debug(f"Executing command: seaweb scrap. Dry run: {context.obj[CONTEXT_DRYRUN]}.")
    execute_seaweb_scrap(context.obj[CONTEXT_DRYRUN])


@main.command(help="Scraper :: run Seaweb parser engine.")
# @click.option()
@click.pass_context
def seaweb_parse(context):
    log.debug(f"Executing command: seaweb parse. Dry run: {context.obj[CONTEXT_DRYRUN]}.")
    execute_seaweb_parse(context.obj[CONTEXT_DRYRUN])


if __name__ == '__main__':
    main(obj={})
