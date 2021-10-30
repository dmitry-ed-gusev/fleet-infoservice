#!/usr/bin/env bash

###############################################################################
#
#   Build and test script for [fleet-db-scraping] utility.
#
#   Created:  Dmitrii Gusev, 23.03.2021
#   Modified: Dmitrii Gusev, 30.10.2021
#
###############################################################################

# -- lock pipenv dependencies (update from file Pipfile.lock)
pipenv lock

# -- run pytest with pytest-cov (see setup.cfg)
pipenv run pytest tests

# -- run mypy - types checker
# todo: put output to separated file?
pipenv run mypy wfleet/

# -- run flake8 for checking code formatting
# todo: put output to separated file?
pipenv run flake8 wfleet/
pipenv run flake8 tests/

# - install virtualenv
#pip3 install virtualenv
# - create virtual environment
#virtualenv --verbose .venv
# - activate virtual environment
#source .venv/bin/activate
# - upgrade pip3 in virtual environment
#python3 -m pip3 install --upgrade pip
# - install necessary dependencies in virtual environment (according to requirements)
#pip3 install -r requirements.txt
# - run unit tests with coverage and XML/HTML reports
#python3 -m nose2 --verbose --start-dir fleet_scraper_tests --plugin nose2.plugins.junitxml \
#    -X --with-coverage --coverage fleet_scraper \
#    --coverage-report xml --junit-xml-path .coverage/nose2-junit.xml --coverage-report html
# - deactivate virtual environment (exit)
#deactivate
