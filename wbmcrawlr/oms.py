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

import requests
from future import standard_library

from wbmcrawlr.urls import OMS_API_URL, OMS_ALTERNATIVE_API_URL

standard_library.install_aliases()

import cernrequests

from wbmcrawlr.utils import flatten_resource, print_progress, calc_page_count, \
    split_filling_scheme

from omsapi import OMSAPI

PAGE_SIZE = 1000

def get_run(run_number, **kwargs):
    filters = [{
        "attribute_name": "run_number",
        "value": run_number,
        "operator": "EQ"
    }]

    if "omsapi" in kwargs:
        omsapi = kwargs["omsapi"]
    else:
        omsapi=OMSAPI()
        omsapi.auth_cert()

    runs_query = omsapi.query("runs")
    runs_query.filters(filters)
    runs_query.sort("run_number", asc=True).include("meta")

    return runs_query.data().json()

def get_fill(fill_number, **kwargs):
    filters = [{
        "attribute_name": "fill_number",
        "value": fill_number,
        "operator": "EQ"
    }]

    if "omsapi" in kwargs:
        omsapi = kwargs["omsapi"]
    else:
        omsapi=OMSAPI()
        omsapi.auth_cert()

    fills_query = omsapi.query("fills")
    fills_query.filters(filters)
    fills_query.sort("fill_number", asc=True).include("meta")

    return fills_query.data().json()

def get_resources(query, table, page_size=PAGE_SIZE, silent=False, **kwargs):
    if not silent:
        print("Getting initial response...", end="\r")

    response = query.paginate(page=1, per_page=page_size).data()
    resource_count = response.json()["meta"]["totalResourceCount"]
    page_count = calc_page_count(resource_count, page_size)

    if not silent:
        print(" " * 100, end="\r")
        print("Total number of {}: {}".format(table, resource_count))
        print()

    resources = [flatten_resource(resource) for resource in response.json()["data"]]

    for page in range(2, page_count + 1):
        if not silent:
            print_progress(page, page_count, text="Page {}/{}".format(page, page_count))
        response = query.paginate(page=page, per_page=page_size).data()

        if response is 200:
            resources.extend([flatten_resource(resource) for resource in response.json()["data"]])
        else:
            print(response)

    if not silent:
        print()
        print()

    assert len(resources) == resource_count, "Oops, not enough resources were returned"
    return resources


def get_runs(begin, end, **kwargs):
    """"
    >>> get_runs(317512, 317512)

    """
    print("Getting runs {} - {} from CMS OMS".format(begin, end))

    filters = [{
        "attribute_name": "run_number",
        "value": begin,
        "operator": "GE"
    },
        {
        "attribute_name": "run_number",
        "value": end,
        "operator": "LE"
    },
        {
        "attribute_name": "sequence",
        "value": "GLOBAL-RUN",
        "operator": "EQ"
    }]

    if "omsapi" in kwargs:
        omsapi = kwargs["omsapi"]
    else:
        omsapi=OMSAPI()
        omsapi.auth_cert()

    runs_query = omsapi.query("runs")
    runs_query.filters(filters)
    runs_query.sort("run_number", asc=True).include("meta")
    runs_query.set_verbose(False)

    return get_resources(runs_query, "runs", page_size=100, **kwargs)


def get_fills(begin, end, **kwargs):
    print("Getting fills {} - {} from CMS OMS".format(begin, end))

    filters = [{
        "attribute_name": "fill_number",
        "value": begin,
        "operator": "GE"
    },
        {
        "attribute_name": "fill_number",
        "value": end,
        "operator": "LE"
    }]

    if "omsapi" in kwargs:
        omsapi = kwargs["omsapi"]
    else:
        omsapi=OMSAPI()
        omsapi.auth_cert()

    fills_query = omsapi.query("fills")
    fills_query.filters(filters)
    fills_query.sort("fill_number", asc=True).include("meta")
    fills_query.set_verbose(False)

    split_scheme = kwargs.pop("split_filling_scheme", False)

    if not split_scheme:
        return get_resources(fills_query, "fills", page_size=100, **kwargs)
    else:
        fills = get_resources(fills_query, "fills", page_size=100, **kwargs)
        for fill in fills:
            split_filling_scheme(fill)
        return fills


def get_lumisection_count(run_number, **kwargs):
    """
    :return: Number of lumisections where CMS was active
    """
    filters = [{
        "attribute_name": "run_number",
        "value": run_number,
        "operator": "EQ"
    }]
    '''
        {
        "attribute_name": "cms_active",
        "value": "true",
        "operator": "EQ"
    }
    '''

    if "omsapi" in kwargs:
        omsapi = kwargs["omsapi"]
    else:
        omsapi=OMSAPI()
        omsapi.auth_cert()

    lumisections_query = omsapi.query("lumisections")
    lumisections_query.filters(filters)
    lumisections_query.sort("lumisection_number", asc=True).include("meta")
    lumisections_query.set_verbose(False)

    response = lumisections_query.data()
    resource_count = response.json()["meta"]["totalResourceCount"]
    return resource_count


def get_lumisections(
    run_number=None, fill_number=None, start_time=None, end_time=None, **kwargs
):
    assert (
        bool(run_number) ^ bool(fill_number) ^ bool(start_time and end_time)
    ), "Specify either run number or fill number or time range"

    filters=[]
    if run_number:
        filters.append({
                "attribute_name": "run_number",
                "value": run_number,
                "operator": "EQ"
            })
    elif fill_number:
        filters.append({
                "attribute_name": "fill_number",
                "value": fill_number,
                "operator": "EQ"
            })
    elif start_time and end_time:
        filters.append({
                "attribute_name": "start_time",
                "value": start_time,
                "operator": "GE"
            })
        filters.append({
                "attribute_name": "end_time",
                "value": end_time,
                "operator": "LE"
            })

    if "omsapi" in kwargs:
        omsapi = kwargs["omsapi"]
    else:
        omsapi=OMSAPI()
        omsapi.auth_cert()

    lumisections_query = omsapi.query("lumisections")
    lumisections_query.filters(filters)
    lumisections_query.sort("lumisection_number", asc=True).include("meta")
    lumisections_query.set_verbose(False)

    return get_resources(lumisections_query, "lumisections", page_size=5000, **kwargs)


def get_hltpathinfos(run_number, **kwargs):
    filters = [{
        "attribute_name": "run_number",
        "value": run_number,
        "operator": "EQ"
    }]

    if "omsapi" in kwargs:
        omsapi = kwargs["omsapi"]
    else:
        omsapi=OMSAPI()
        omsapi.auth_cert()

    hltpathinfo_query = omsapi.query("hltpathinfo")
    hltpathinfo_query.filters(filters)
    hltpathinfo_query.include("meta")
    hltpathinfo_query.set_verbose(False)

    return get_resources(hltpathinfo_query, "hltpathinfo", page_size=1000, **kwargs)


def get_hltpathrates(run_number, path_name, **kwargs):
    filters = [{
        "attribute_name": "last_lumisection_number",
        "value": 0,
        "operator": "GT"
    },
        {
        "attribute_name": "path_name",
        "value": path_name,
        "operator": "EQ"
    },
        {
        "attribute_name": "run_number",
        "value": run_number,
        "operator": "EQ"
    }]

    if "omsapi" in kwargs:
        omsapi = kwargs["omsapi"]
    else:
        omsapi=OMSAPI()
        omsapi.auth_cert()

    hltpathrates_query = omsapi.query("hltpathrates")
    hltpathrates_query.filters(filters)
    hltpathrates_query.custom("group[granularity]","lumisection")
    hltpathrates_query.sort("last_lumisection_number", asc=True).include("meta")
    hltpathrates_query.set_verbose(False)

    return get_resources(hltpathrates_query, "hltpathrates", page_size=10000, **kwargs)

def get_all_hltpathrates(run_number, silent=False, **kwargs):
    if not silent:
        print("Retrieving all hltpathrates for run number {}".format(run_number))
        print("Getting list of available hltpathinfos...")

    hltpathinfos = get_hltpathinfos(run_number, silent=True, **kwargs)

    path_info_count = len(hltpathinfos)

    path_names = [pathinfo["path_name"] for pathinfo in hltpathinfos]

    hltpathrates = []

    for i, path_name in enumerate(path_names, 1):

        print_progress(
            i,
            path_info_count,
            text="Path {}/{}: {:80s}".format(i, path_info_count, path_name),
        )
        hltpathrates.extend(
            get_hltpathrates(run_number, path_name, silent=True, **kwargs)
        )

    return hltpathrates
