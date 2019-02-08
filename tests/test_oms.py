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

from wbmcrawlr import oms


def test_get_run():
    run = oms.get_run(327564)

    assert run["id"] == "327564"
    assert run["attributes"]["delivered_lumi"] == 8.117866
    assert run["attributes"]["recorded_lumi"] == 7.763654
    assert run["attributes"]["l1_key"] == "l1_trg_collisionshi2018/v28"


def test_get_runs():
    runs = oms.get_runs(326941, 326942)
    assert len(runs) == 2
    assert runs[0]["run_number"] == 326941
    assert runs[1]["run_number"] == 326942


def test_get_runs_big_range():
    runs = oms.get_runs(326741, 326942)
    assert len(runs) == 117


def test_get_fill():
    fill = oms.get_fill(7492)
    assert fill["id"] == "7492"
    assert fill["attributes"]["fill_number"] == 7492
    assert fill["attributes"]["fill_type_runtime"] == "PB"
    assert fill["attributes"]["energy"] == 6369
    assert fill["attributes"]["delivered_lumi"] == 8.107441
    assert fill["attributes"]["recorded_lumi"] == 7.753413
    assert fill["attributes"]["crossing_angle"] == 160


def test_get_fills():
    fills = oms.get_fills(7480, 7483)
    assert len(fills) == 4
    assert fills[0]["fill_number"] == 7480
    assert fills[1]["fill_number"] == 7481
    assert fills[2]["fill_number"] == 7482
    assert fills[3]["fill_number"] == 7483


def test_get_fills_big_range():
    fills = oms.get_fills(7000, 7495)
    assert len(fills) == 158
