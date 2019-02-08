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
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library

standard_library.install_aliases()
import argparse
import json
import os

from wbmcrawlr import oms
from wbmcrawlr.utils import save_to_disk, flatten_run


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="CERN CMS WBM and OMS crawler.",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=36),
    )

    parser.add_argument("min", help="Minimum run number")
    parser.add_argument("max", help="Maximum run number")

    resource_group = parser.add_mutually_exclusive_group(required=True)
    resource_group.add_argument("--runs", help="Retrieve Runs", action="store_true")
    resource_group.add_argument("--fills", help="Retrieve Fills", action="store_true")

    return parser.parse_args()


def crawl_run(run_number):
    run = oms.get_run(run_number)
    file_name = "{}_{}.json".format("oms", run_number)
    path = os.path.join("oms", file_name)
    content = json.dumps(run, indent=2)
    save_to_disk(path, content=content)
    return flatten_run(run)


def main():
    args = parse_arguments()
    min = args.min
    max = args.max

    method = oms.get_runs if args.runs else oms.get_fills
    resource = "runs" if args.runs else "fills"
    response = method(min, max)

    content = json.dumps(response, indent=2)

    filename = "oms_{}.json".format(resource)
    save_to_disk(filename, content=content)
    print("Stored {} {} in '{}'".format(len(response), resource, filename))


if __name__ == "__main__":
    main()
