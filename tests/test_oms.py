from wbmcrawlr import oms


def test_get_run():
    run = oms.get_run(327564)

    assert run["id"] == "327564"
    assert run["attributes"]["delivered_lumi"] == 8.117866
    assert run["attributes"]["recorded_lumi"] == 7.763654


def test_get_runs():
    runs = oms.get_runs(326941, 326942)
    assert len(runs) == 2
    assert runs[0]["run_number"] == 326941
    assert runs[1]["run_number"] == 326942


def test_get_runs_big_range():
    runs = oms.get_runs(326741, 326942)
    assert len(runs) == 117
