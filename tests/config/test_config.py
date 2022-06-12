#!/usr/bin/env python3
# coding=utf-8

"""
    Unit tests for scraper_config.py module.

    Created:  Dmitrii Gusev, 12.12.2021
    Modified: Dmitrii Gusev, 25.12.2021
"""

from pathlib import Path
from importlib import reload

import wfleet.scraper.config.scraper_config as sconfig
import wfleet.scraper.config.logging_config as lconfig


def mock_return_true(path):  # helper mock method
    return True


def mock_return_false(path):  # helper mock method
    return False


def mock_return_home_dir():  # helper mock method
    return Path("/dummy/home/dir")


def _test_scraper_config_local_dir(monkeypatch):
    monkeypatch.setattr(Path, "exists", mock_return_true)
    monkeypatch.setattr(Path, "is_dir", mock_return_true)

    reload(sconfig)  # reload CONFIG for safe tests run
    reload(lconfig)  # reload LOGGER_CONFIG for safe tests run

    # assert - check cache dir path
    assert ".wfleet" == sconfig.CONFIG["cache_dir"]
    assert ".wfleet/logs" == sconfig.CONFIG["cache_logs_dir"]
    assert ".wfleet/.scraper_raw_files" == \
        sconfig.CONFIG["cache_raw_files_dir"]
    assert ".wfleet/logs/log_info.log" == \
        lconfig.LOGGING_CONFIG["handlers"]["std_file_handler"]["filename"]
    assert ".wfleet/logs/log_errors.log" == \
        lconfig.LOGGING_CONFIG["handlers"]["error_file_handler"]["filename"]


def _test_scraper_config_home_dir_not_exists_not_a_dir(monkeypatch):

    monkeypatch.setattr(Path, "exists", mock_return_false)
    monkeypatch.setattr(Path, "is_dir", mock_return_false)
    monkeypatch.setattr(Path, "home", mock_return_home_dir)

    reload(sconfig)  # reload CONFIG for safe tests run
    reload(lconfig)  # reload LOGGER_CONFIG for safe tests run

    # assert - check cache dir path
    assert "/dummy/home/dir/.wfleet" == sconfig.CONFIG["cache_dir"]
    assert "/dummy/home/dir/.wfleet/logs" == sconfig.CONFIG["cache_logs_dir"]
    assert "/dummy/home/dir/.wfleet/.scraper_raw_files" == \
        sconfig.CONFIG["cache_raw_files_dir"]
    assert "/dummy/home/dir/.wfleet/logs/log_info.log" == \
        lconfig.LOGGING_CONFIG["handlers"]["std_file_handler"]["filename"]
    assert "/dummy/home/dir/.wfleet/logs/log_errors.log" == \
        lconfig.LOGGING_CONFIG["handlers"]["error_file_handler"]["filename"]


def _test_scraper_config_home_dir_exists_not_a_dir(monkeypatch):
    
    monkeypatch.setattr(Path, "exists", mock_return_true)
    monkeypatch.setattr(Path, "is_dir", mock_return_false)
    monkeypatch.setattr(Path, "home", mock_return_home_dir)

    reload(sconfig)  # reload CONFIG for safe tests run
    reload(lconfig)  # reload LOGGER_CONFIG for safe tests run

    # assert - check cache dir path
    assert "/dummy/home/dir/.wfleet" == sconfig.CONFIG["cache_dir"]
    assert "/dummy/home/dir/.wfleet/logs" == sconfig.CONFIG["cache_logs_dir"]
    assert "/dummy/home/dir/.wfleet/.scraper_raw_files" == \
        sconfig.CONFIG["cache_raw_files_dir"]
    assert "/dummy/home/dir/.wfleet/logs/log_info.log" == \
        lconfig.LOGGING_CONFIG["handlers"]["std_file_handler"]["filename"]
    assert "/dummy/home/dir/.wfleet/logs/log_errors.log" == \
        lconfig.LOGGING_CONFIG["handlers"]["error_file_handler"]["filename"]
        
        
def _test_scraper_config_home_dir_not_exists_is_a_dir(monkeypatch):  # dummy case :)
    
    monkeypatch.setattr(Path, "exists", mock_return_false)
    monkeypatch.setattr(Path, "is_dir", mock_return_true)
    monkeypatch.setattr(Path, "home", mock_return_home_dir)

    reload(sconfig)  # reload CONFIG for safe tests run
    reload(lconfig)  # reload LOGGER_CONFIG for safe tests run

    # assert - check cache dir path
    assert "/dummy/home/dir/.wfleet" == sconfig.CONFIG["cache_dir"]
    assert "/dummy/home/dir/.wfleet/logs" == sconfig.CONFIG["cache_logs_dir"]
    assert "/dummy/home/dir/.wfleet/.scraper_raw_files" == \
        sconfig.CONFIG["cache_raw_files_dir"]
    assert "/dummy/home/dir/.wfleet/logs/log_info.log" == \
        lconfig.LOGGING_CONFIG["handlers"]["std_file_handler"]["filename"]
    assert "/dummy/home/dir/.wfleet/logs/log_errors.log" == \
        lconfig.LOGGING_CONFIG["handlers"]["error_file_handler"]["filename"]
