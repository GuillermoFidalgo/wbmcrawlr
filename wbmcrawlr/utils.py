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

from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import open

import cernrequests
import requests
from future import standard_library

from wbmcrawlr.constants import TIMEOUT_TIME
from wbmcrawlr.urls import OMS_API_URL, OMS_ALTERNATIVE_API_URL

standard_library.install_aliases()
import math
import os
import sys


def save_to_disk(path, content):
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        print("Creating directory '{}'".format(directory))
        os.makedirs(directory)
    with open(path, "w") as file:
        try:
            file.write(content)
        except TypeError:
            file.write(content.decode("utf-8"))


def flatten_resource(response):
    response_flat = response["attributes"]
    if response["type"] in ["runs", "fills"]:
        for key, value in response["meta"]["row"].items():
            new_field_name = "{}_unit".format(key)
            response_flat.update({new_field_name: value["units"]})
    return response_flat


def progress_bar(current, total, text="", filler="#"):
    bar_length = 50
    processed = current / total
    processed_length = math.ceil(processed * bar_length)

    bar = filler * processed_length + "-" * (bar_length - processed_length)

    return "[{}] {:.2%} {}".format(bar, processed, text)


def print_progress(current, total, text="", *args, **kwargs):
    print(progress_bar(current, total, text, *args, **kwargs), end="\r")
    sys.stdout.flush()


def check_connectivity(url):
    """
    Check if url can be accessed.

    :return: True if url can be accessed
    """
    try:
        requests.get(url, timeout=TIMEOUT_TIME)
        return True
    except requests.exceptions.ConnectTimeout:
        return False


def check_oms_connectiviy():
    return check_connectivity(OMS_API_URL)


def get_oms_cookie(silent=False):
    url = OMS_ALTERNATIVE_API_URL
    if not silent:
        print("Getting SSO Cookie for {}...".format(url))
    return cernrequests.get_sso_cookies(url)


def calc_page_count(resource_count, page_size):
    return math.ceil(resource_count / page_size)
