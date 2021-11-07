#!/usr/bin/env bash

###############################################################################
#
#   Build and test script for [fleet-db-scraping] utility.
#
#   Created:  Dmitrii Gusev, 23.03.2021
#   Modified: Dmitrii Gusev, 07.11.2021
#
###############################################################################

# todo: do put output of utilities - mypy/black/flake8 - to a separated file(s)?

# -- clean caches and sync + lock pipenv dependencies (update from the file Pipfile.lock)
pipenv --verbose clean
pipenv --verbose update

# -- run pytest with pytest-cov (see pytest.ini/setup.cfg - additional parameters)
pipenv run pytest tests/

# -- run mypy - types checker

pipenv run mypy src/
pipenv run mypy tests/

# -- run black code formatter
pipenv run black src/ --verbose --line-length 110
pipenv run black tests/ --verbose --line-length 110

# -- run flake8 for checking code formatting
pipenv run flake8 src/
pipenv run flake8 tests/
