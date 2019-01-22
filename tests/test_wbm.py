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

from wbmcrawlr import wbm


def assert_run_info_properties(run_info):
    desired_properties = [
        "runLumi",
        "runLiveLumi",
        "liveLumi",
        "recordedLumi",
        "eff",
        "lhcFill",
        "fill",
        "lhcEnergy",
        "initLumi",
        "endLumi",
        "lumiFillEnd",
        "lumiFillBegin",
        "liveLumiFillEnd",
        "liveLumiFillBegin",
    ]

    for name in desired_properties:
        assert name in run_info


def test_run_summary():
    run_summary = wbm.get_run_summary(327564)
    run_info = run_summary["cmsdb"]["runInfo"]

    assert run_info["runLumi"] == "8.117866"
    assert run_info["runLiveLumi"] == "7.763654"
    assert run_info["recordedLumi"] == "7.76365353"
    assert run_info["delivLumi"] == "8.11786577"
    assert run_info["liveLumi"] == "7.76365353"


def test_run_summary_old_run():
    run_summary = wbm.get_run_summary(211831)
    run_info = run_summary["cmsdb"]["runInfo"]

    assert run_info["bField"] == "3.80056399"
    assert run_info["run"] == "211831"
    assert run_info["nLumiSections"] == "160"

    assert_run_info_properties(run_info)


def test_run_range():
    run_summary = wbm.get_run_summary_by_range(211831, 211851)
    run_infos = run_summary["cmsdb"]["runInfo"]
    assert len(run_infos) == 9

    # Apparently they are ordered in reverse
    assert run_infos[8]["bField"] == "3.80056399"
    assert run_infos[8]["run"] == "211831"
    assert run_infos[8]["nLumiSections"] == "160"
    assert run_infos[7]["run"] == "211835"
    assert run_infos[0]["run"] == "211850"

    for run_info in run_infos:
        assert_run_info_properties(run_info)
