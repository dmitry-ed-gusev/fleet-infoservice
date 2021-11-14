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
#   Modified: Dmitrii Gusev, 14.11.2021
#
###############################################################################

export LANG='en_US.UTF-8'
BUILD_DIR='build/'
DIST_DIR='dist/'

echo "Development Environment setup started..."

# - remove existing virtual environment, clear caches
echo "Deleting virtual environment and clearing caches."
pipenv --rm
pipenv --clear

# - clean build and distribution folders
echo "Deleting ${BUILD_DIR}..."
rm -r "${BUILD_DIR}"
echo "Deleting ${DIST_DIR}..."
rm -r "${DIST_DIR}"

# - install all dependencies, including development + update
echo "Installing pipenv dependencies, updating outdated."
pipenv install --dev
pipenv update
# - update outdated dependencies
pipenv update --outdated

# - check for vulnerabilities and show dependencies graph
echo "Checking virtual environment for vulnerabilities."
pipenv check
pipenv graph
