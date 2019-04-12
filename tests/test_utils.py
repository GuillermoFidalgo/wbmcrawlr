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

from wbmcrawlr.utils import flatten_resource, progress_bar, calc_page_count, split_filling_scheme


def test_flatten():
    run = {
        "id": "123456",
        "type": "runs",
        "attributes": {
            "components": [
                "CASTOR",
                "CSC",
                "DAQ",
                "DCS",
                "DQM",
                "DT",
                "ECAL",
                "ES",
                "GEM",
                "HCAL",
                "PIXEL",
                "RPC",
                "SCAL",
                "TCDS",
                "TRACKER",
                "TRG",
            ],
            "l1_hlt_mode_stripped": "collisionshi2018/v99",
            "duration": 5471,
            "b_field": 3.8,
            "tier0_transfer": True,
            "l1_triggers_counter": 58916273,
            "hlt_physics_throughput": 1.20394707,
            "init_lumi": 2.22189,
            "delivered_lumi": 6.628991,
            "recorded_lumi": 5.469869,
            "cmssw_version": "CMSSW_10_3_1",
            "energy": 6369.0,
            "end_lumi": 2.175897,
            "hlt_physics_rate": 1335.808,
            "fill_number": 7456,
            "end_time": "2018-11-19T22:08:01Z",
            "l1_key_stripped": "collisionshi2018/v24",
            "initial_prescale_index": 0,
            "sequence": "GLOBAL-RUN",
            "start_time": "2018-11-19T20:36:50Z",
            "hlt_physics_size": 6510.964,
            "fill_type_runtime": "PB",
            "hlt_key": "/cdaq/physics/Run2018HI/v1.5.0/HLT/V13",
            "clock_type": "LHC",
            "l1_rate": 10847.697,
            "l1_menu": "L1Menu_HeavyIon2018",
            "run_number": 123456,
            "stable_beam": True,
            "hlt_physics_counter": 7224070.0,
        },
        "links": {"self": "http://cmsomsrproxyext.cern.ch/api/v1/runs/123456"},
        "meta": {
            "row": {
                "b_field": {"units": "T"},
                "init_lumi": {"units": "10^{27}cm^{-2}s^{-1}"},
                "delivered_lumi": {"units": "{\\mu}b^{-1}"},
                "recorded_lumi": {"units": "{\\mu}b^{-1}"},
                "end_lumi": {"units": "10^{27}cm^{-2}s^{-1}"},
                "energy": {"units": "GeV"},
            }
        },
    }

    flat_run = flatten_resource(run)

    assert flat_run == {
        "run_number": 123456,
        "components": [
            "CASTOR",
            "CSC",
            "DAQ",
            "DCS",
            "DQM",
            "DT",
            "ECAL",
            "ES",
            "GEM",
            "HCAL",
            "PIXEL",
            "RPC",
            "SCAL",
            "TCDS",
            "TRACKER",
            "TRG",
        ],
        "l1_hlt_mode_stripped": "collisionshi2018/v99",
        "duration": 5471,
        "b_field": 3.8,
        "tier0_transfer": True,
        "l1_triggers_counter": 58916273,
        "hlt_physics_throughput": 1.20394707,
        "init_lumi": 2.22189,
        "delivered_lumi": 6.628991,
        "recorded_lumi": 5.469869,
        "cmssw_version": "CMSSW_10_3_1",
        "energy": 6369.0,
        "end_lumi": 2.175897,
        "hlt_physics_rate": 1335.808,
        "fill_number": 7456,
        "end_time": "2018-11-19T22:08:01Z",
        "l1_key_stripped": "collisionshi2018/v24",
        "initial_prescale_index": 0,
        "sequence": "GLOBAL-RUN",
        "start_time": "2018-11-19T20:36:50Z",
        "hlt_physics_size": 6510.964,
        "fill_type_runtime": "PB",
        "hlt_key": "/cdaq/physics/Run2018HI/v1.5.0/HLT/V13",
        "clock_type": "LHC",
        "l1_rate": 10847.697,
        "l1_menu": "L1Menu_HeavyIon2018",
        "stable_beam": True,
        "hlt_physics_counter": 7224070.0,
        "b_field_unit": "T",
        "init_lumi_unit": "10^{27}cm^{-2}s^{-1}",
        "delivered_lumi_unit": "{\\mu}b^{-1}",
        "recorded_lumi_unit": "{\\mu}b^{-1}",
        "end_lumi_unit": "10^{27}cm^{-2}s^{-1}",
        "energy_unit": "GeV",
    }


def test_progress_bar():
    assert (
        "[--------------------------------------------------] 0.00% "
        == progress_bar(0, 100)
    )
    assert (
        "[########------------------------------------------] 15.00% "
        == progress_bar(15, 100)
    )
    assert (
        "[########------------------------------------------] 15.00% "
        == progress_bar(7.5, 50)
    )
    assert (
        "[#################---------------------------------] 33.33% bla"
        == progress_bar(2, 6, "bla")
    )
    assert (
        "[======================----------------------------] 42.42% "
        == progress_bar(4242, 10000, filler="=")
    )
    assert (
        "[##################################################] 100.00% "
        == progress_bar(5, 5)
    )


def test_calc_page_count():
    assert 0 == calc_page_count(0, 100)
    assert 1 == calc_page_count(1, 100)
    assert 1 == calc_page_count(17, 100)
    assert 1 == calc_page_count(99, 100)
    assert 1 == calc_page_count(100, 100)
    assert 2 == calc_page_count(101, 100)

def test_split_filling_scheme():
    data = {
     'era': 'HIRun2018A',
     'bunches_target': 733,
     'injection_scheme': '75_150ns_733Pb_733_702_468_42bpi_20inj',
     'delivered_lumi': 71.478508}

    split_filling_scheme(data)

    # Assert new fields

    assert data["injection_scheme_spacing"] == '75'
    assert data["injection_scheme_bunches"] == '150ns'
    assert data["injection_scheme_ip1_5"] == '733Pb'
    assert data["injection_scheme_ip2"] == '733'
    assert data["injection_scheme_ip8"] == '702'
    assert data["injection_scheme_trainlength"] == '468'
    assert data["injection_scheme_injections"] == '42bpi'
    assert data["injection_scheme_special_info"] == '20inj'

    assert data['injection_scheme'] == '75_150ns_733Pb_733_702_468_42bpi_20inj'

    # Assert no change in old data
    assert data['era'] == 'HIRun2018A'
    assert data['bunches_target'] == 733
    assert data['injection_scheme'] == '75_150ns_733Pb_733_702_468_42bpi_20inj'


def test_split_filling_scheme_2():
        data = {
            'era': 'HIRun2018A',
            'bunches_target': 733,
            'injection_scheme': '100_150ns_648Pb_620_619_52_36bpi_20inj_V2',
            'delivered_lumi': 71.478508}

        split_filling_scheme(data)

        # Assert new fields

        assert data["injection_scheme_spacing"] == '100'
        assert data["injection_scheme_bunches"] == '150ns'
        assert data["injection_scheme_ip1_5"] == '648Pb'
        assert data["injection_scheme_ip2"] == '620'
        assert data["injection_scheme_ip8"] == '619'
        assert data["injection_scheme_trainlength"] == '52'
        assert data["injection_scheme_injections"] == '36bpi'
        assert data["injection_scheme_special_info"] == '20inj'

        # Assert no change in old data
        assert data['era'] == 'HIRun2018A'
        assert data['bunches_target'] == 733
        assert data['injection_scheme'] == '100_150ns_648Pb_620_619_52_36bpi_20inj_V2'


