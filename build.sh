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
