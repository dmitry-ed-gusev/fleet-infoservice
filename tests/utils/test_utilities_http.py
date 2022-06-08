#!/usr/bin/env python3
# coding=utf-8

"""
    Unit tests for http utilities.

    Created:  Dmitrii Gusev, 02.06.2021
    Modified: Dmitrii Gusev, 05.06.2022
"""

import pytest
from wfleet.scraper.utils.utilities_http import (
    # perform_file_download_over_http,
    perform_file_download_over_http,
    process_url,
    # process_urls,
)


@pytest.mark.parametrize("value", [None, '', '    ', 'asdf'])
def test_perform_file_download_over_http_invalid_url(value):
    with pytest.raises(ValueError):
        perform_file_download_over_http(value, "dir")


# todo: fix the test - use responses module
# @responses.activate
# def test_downloads_file(self):
#     url = 'http://example.org/excel.xls'
#     with open('./utils_test_files/excel.xls', 'rb') as excel_file:
#         responses.add(responses.GET, url,
#                       body=excel_file.read(), status=200,
#                       content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
#                       adding_headers={'Transfer-Encoding': 'chunked'})
#         filename = perform_file_download_over_http(url, './zzz/aaa')
#         # assert things here.


@pytest.mark.parametrize("url, postfix, format_params, expected", [
        ('http://myurl/', '123456', None, 'http://myurl/123456'),
        ('http://myurl', '123456', None, 'http://myurl/123456'),
        ('http://myurl{}/suburl/', '', ('xxx',), 'http://myurlxxx/suburl/'),
        ('http://myurl{}/suburl/', '', ('xxx', 'zzz'), 'http://myurlxxx/suburl/'),
        ('http://myurl{}/suburl{}/{}', '', ('aaa', 'bbb', 'ccc',), 'http://myurlaaa/suburlbbb/ccc'),
        ('http://myurl{}/suburl{}/{}', '', ('aaa', 'bbb', 'ccc', 'www'), 'http://myurlaaa/suburlbbb/ccc'),
        ('http://myurl{}/suburl{}/{}', '2', ('_a', '_b', '_c',), 'http://myurl_a/suburl_b/_c/2'),
    ]
)
def test_process_url(url, postfix, format_params, expected):
    assert process_url(url, postfix, format_params) == expected
