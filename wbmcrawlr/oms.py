#!/usr/bin/python
# -*- coding: utf-8 -*-

# © Copyright 2018 CERN
#
# This software is distributed under the terms of the GNU General Public
# Licence version 3 (GPL Version 3), copied verbatim in the file “LICENSE”
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""
Retrieve runs from the CMS Online Monitoring System
https://cmsoms.cern.ch/cms/runs/report
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import range
from urllib.parse import urlencode

from future import standard_library

standard_library.install_aliases()
import math

import cernrequests
from cernrequests import get_sso_cookies

from wbmcrawlr.utils import flatten_resource, print_progress

OMS_API_URL = "https://cmsoms.cern.ch/agg/api/v1/"
PAGE_SIZE = 100


def get_resource(table, parameters):
    parameters = urlencode(parameters)
    url = "{base}{table}?{parameters}".format(
        base=OMS_API_URL, table=table, parameters=parameters
    )

    cookies = get_sso_cookies(url)
    response = cernrequests.get(url, cookies=cookies)

    data = response.json()["data"]
    assert len(data) == 1, "More than 1 {} were returned".format(table)

    return data[0]


def get_run(run_number):
    parameters = {"filter[run_number][EQ]": run_number, "sort": "-run_number"}
    return get_resource("runs", parameters)


def get_fill(fill_number):
    parameters = {"filter[fill_number][EQ]": fill_number, "sort": "-fill_number"}
    return get_resource("fills", parameters)


def _get_resources(table, parameters, cookies, page=0):
    parameters = urlencode(
        {"page[offset]": page * PAGE_SIZE, "page[limit]": PAGE_SIZE}.update(parameters)
    )

    url = "{base}{table}?{parameters}".format(
        base=OMS_API_URL, table=table, parameters=parameters
    )

    response = cernrequests.get(url, cookies=cookies)
    return response.json()


def get_resources(table, parameters):
    cookies = get_sso_cookies(OMS_API_URL)

    response = _get_resources(table, parameters, cookies)
    resource_count = response["meta"]["totalResourceCount"]
    page_count = math.ceil(resource_count / PAGE_SIZE)

    print("Total number of {}: {}".format(table, resource_count))
    print()

    resources = [flatten_resource(resource) for resource in response["data"]]

    for page in range(1, page_count + 1):
        print_progress(page, page_count, text="Page {}/{}".format(page, page_count))
        response = _get_resources(table, parameters, cookies, page)
        resources.extend([flatten_resource(resource) for resource in response["data"]])

    print()
    print()
    return resources


def get_runs(begin, end):
    print("Getting runs {} - {} from CMS OMS".format(begin, end))
    parameters = {
        "filter[run_number][GE]": begin,
        "filter[run_number][LE]": end,
        "filter[sequence][EQ]": "GLOBAL-RUN",
        "sort": "run_number",
    }

    return get_resources("runs", parameters)


def get_fills(begin, end):
    print("Getting fills {} - {} from CMS OMS".format(begin, end))
    parameters = {
        "filter[fill_number][GE]": begin,
        "filter[fill_number][LE]": end,
        "filter[start_stable_beam][NEQ]": "null",
        "sort": "fill_number",
    }

    return get_resources("fills", parameters)
