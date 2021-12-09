#!/usr/bin/env bash

###############################################################################
#
#   Development environment setup script. Script can be used to re-create
#   development environment fro 'scratch'.
#
#   Warning: script must be used (run) from shell, not from the virtual
#            environment (pipenv shell).
#
#   Created:  Dmitrii Gusev, 13.11.2021
#   Modified: Dmitrii Gusev, 09.12.2021
#
###############################################################################

# todo: add verbosity flag
# todo: add installation of ipykernel + local kernel
# todo: add pip upgrade command (?)

export LANG='en_US.UTF-8'
BUILD_DIR='build/'
DIST_DIR='dist/'

echo "Development Environment setup started..."
echo
echo

# - remove existing virtual environment, clear caches
echo "Deleting virtual environment and clearing caches."
pipenv --rm
pipenv --clear

# - clean build and distribution folders
echo "Deleting ${BUILD_DIR}..."
rm -r "${BUILD_DIR}"
echo "Deleting ${DIST_DIR}..."
rm -r "${DIST_DIR}"

# - removing Pipfile.lock
echo "Removing Pipfile.lock"
rm Pipfile.lock

# - install all dependencies, incl. development + update, incl. outdated
echo "Installing dependencies, updating + updating outdated."
#pipenv clean
pipenv lock
pipenv install --dev
pipenv update
pipenv update --outdated

# - check for vulnerabilities and show dependencies graph
echo "Checking virtual environment for vulnerabilities."
pipenv check
pipenv graph

# - outdated packages report
pipenv run pip list --outdated
