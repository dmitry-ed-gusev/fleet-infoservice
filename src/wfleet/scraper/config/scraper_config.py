#!/usr/bin/env python3
# coding=utf-8

"""
    World Fleet Scraper configuration for the application.
    Useful materials:
      - https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b

    Created:  Gusev Dmitrii, 12.12.2021
    Modified: Dmitrii Gusev, 14.12.2021
"""

from pathlib import Path

CACHE_DIR_NAME = ".wfleet"

# define cache position - in the current dir or in the home dir
cache_path: Path = Path(CACHE_DIR_NAME)
prefix: str = ""
if not cache_path.exists() or not cache_path.is_dir():
    prefix = str(Path.home()) + "/"

# configuration dictionary
CONFIG = {
    "encoding": "utf-8",
    "cache_dir": f"{prefix}{CACHE_DIR_NAME}",
}


if __name__ == "__main__":
    print("Don't run configuration module directly!")
