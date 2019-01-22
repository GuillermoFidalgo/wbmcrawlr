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
    run_min = args.min
    run_max = args.max
    runs = oms.get_runs(run_min, run_max)

    content = json.dumps(runs, indent=2)
    filename = "oms_runs.json"
    save_to_disk(filename, content=content)
    print("Stored {} runs in '{}'".format(len(runs), filename))


if __name__ == "__main__":
    main()
