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
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import range
from future import standard_library

standard_library.install_aliases()
import math

import cernrequests
from cernrequests import get_sso_cookies

from wbmcrawlr.utils import flatten_run, print_progress

OMS_API_URL = "https://cmsoms.cern.ch/agg/api/v1/"
PAGE_SIZE = 100

runs_fields = [
    "run_number",
    "fill_number",
    "stable_beam",
    "fill_type_runtime",
    "duration",
    "start_time",
    "end_time",
    "delivered_lumi",
    "recorded_lumi",
    "init_lumi",
    "end_lumi",
    "b_field",
    "energy",
    "clock_type",
    "sequence",
    "l1_hlt_mode_stripped",
    "cmssw_version",
    "initial_prescale_index",
    "tier0_transfer",
    "l1_key_stripped",
    "l1_menu",
    "l1_triggers_counter",
    "l1_rate",
    "hlt_key",
    "hlt_physics_size",
    "hlt_physics_rate",
    "hlt_physics_counter",
    "hlt_physics_throughput",
    "components",
]

runs_fields_string = ",".join(runs_fields)


# delivered_lumi = Run Lumi
# recorded_lumi = Run Live Lumi


def get_run(run_number):
    parameters = ("filter[run_number][EQ]={run_number}&sort=-run_number").format(
        run_number=run_number
    )

    url = "{base}{table}?{parameters}".format(
        base=OMS_API_URL, table="runs", parameters=parameters
    )

    cookies = get_sso_cookies(url)
    response = cernrequests.get(url, cookies=cookies)

    data = response.json()["data"]
    assert len(data) == 1, "More than 1 run were returned"

    return data[0]


def _get_runs(begin, end, cookies, page=0):
    parameters = (
        "page[offset]={page}&page[limit]={page_size}&"
        "&filter[run_number][GE]={begin}"
        "&filter[run_number][LE]={end}"
        "&filter[sequence][EQ]=GLOBAL-RUN"
        "&sort=run_number"
    ).format(begin=begin, end=end, page=page * PAGE_SIZE, page_size=PAGE_SIZE)

    url = "{base}{resource}?{parameters}".format(
        base=OMS_API_URL, resource="runs", parameters=parameters
    )

    response = cernrequests.get(url, cookies=cookies)
    return response.json()


def get_runs(begin, end):
    print("Getting runs {} - {} from CMS OMS".format(begin, end))
    cookies = get_sso_cookies("https://cmsoms.cern.ch")
    response = _get_runs(begin, end, cookies)
    run_count = response["meta"]["totalResourceCount"]
    page_count = math.ceil(run_count / PAGE_SIZE)

    print("Total number of runs: {}".format(run_count))
    print()

    runs = []
    for run in response["data"]:
        runs.append(flatten_run(run))

    for page in range(1, page_count + 1):
        print_progress(page, page_count, text="Page {}/{}".format(page, page_count))
        response = _get_runs(begin, end, cookies, page)
        for run in response["data"]:
            runs.append(flatten_run(run))
    print()
    print()
    return runs


def get_fill(fill_number):
    parameters = "filter[fill_number][EQ]={fill_number}&sort=-fill_number".format(
        fill_number=fill_number
    )

    url = "{base}{table}?{parameters}".format(
        base=OMS_API_URL, table="fills", parameters=parameters
    )

    cookies = get_sso_cookies(url)
    response = cernrequests.get(url, cookies=cookies)

    data = response.json()["data"]
    assert len(data) == 1, "More than 1 fill were returned"

    return data[0]


def _get_fills(begin, end, cookies, page=0):
    parameters = (
        "page[offset]={page}&page[limit]={page_size}&"
        "&filter[fill_number][GE]={begin}"
        "&filter[fill_number][LE]={end}"
        "&filter[start_stable_beam][NEQ]=null"
        "&sort=fill_number"
    ).format(begin=begin, end=end, page=page * PAGE_SIZE, page_size=PAGE_SIZE)

    url = "{base}{resource}?{parameters}".format(
        base=OMS_API_URL, resource="fills", parameters=parameters
    )

    response = cernrequests.get(url, cookies=cookies)
    return response.json()


def get_fills(begin, end):
    print("Getting fills {} - {} from CMS OMS".format(begin, end))
    cookies = get_sso_cookies("https://cmsoms.cern.ch")
    response = _get_fills(begin, end, cookies)
    fill_count = response["meta"]["totalResourceCount"]
    page_count = math.ceil(fill_count / PAGE_SIZE)

    print("Total number of fills: {}".format(fill_count))
    print()

    fills = []
    for fill in response["data"]:
        fills.append(flatten_run(fill))

    for page in range(1, page_count + 1):
        print_progress(page, page_count, text="Page {}/{}".format(page, page_count))
        response = _get_fills(begin, end, cookies, page)
        for fill in response["data"]:
            fills.append(flatten_run(fill))
    print()
    print()
    return fills
