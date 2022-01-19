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
#   Modified: Dmitrii Gusev, 19.01.2022
#
###############################################################################

# -- verbose output mode
VERBOSE="--verbose"
# -- set up encoding/language
export LANG='en_US.UTF-8'
BUILD_DIR='build/'
DIST_DIR='dist/'
# -- local ipykernel name
IPYKERNEL_NAME='fleet-service-kernel'

clear
printf "Development Virtual Environment setup is starting...\n\n"

# -- upgrading pipenv (just for the case)
echo "Upgrading pipenv."
pip install --upgrade pipenv

# -- remove existing virtual environment, clear caches
echo "Deleting virtual environment and clearing caches."
pipenv --rm ${VERBOSE}
pipenv --clear ${VERBOSE}

# -- clean build and distribution folders
echo "Clearing temporary directories."
echo "Deleting ${BUILD_DIR}..."
rm -r "${BUILD_DIR}"
echo "Deleting ${DIST_DIR}..."
rm -r "${DIST_DIR}"

# -- removing Pipfile.lock (re-generate it)
echo "Removing Pipfile.lock"
rm Pipfile.lock

# -- install all dependencies, incl. development
echo "Installing dependencies, updating all + outdated."
pipenv lock ${VERBOSE}
pipenv install --dev ${VERBOSE}

# -- install local ipykernel
echo "Installing local ipykernel + check"
pipenv run ipython kernel install --user --name=${IPYKERNEL_NAME}
# -- list installed ipykernels
jupyter kernelspec list

# -- update all + outdated
#pipenv update --clear ${VERBOSE}
pipenv update --outdated --clear ${VERBOSE}

# - check for vulnerabilities and show dependencies graph
echo "Checking virtual environment for vulnerabilities."
pipenv check
pipenv graph

# - outdated packages report
echo
echo "Outdated packages list:"
pipenv run pip list --outdated
echo
