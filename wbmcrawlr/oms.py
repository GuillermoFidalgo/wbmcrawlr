"""
Retrieve runs from the CMS Online Monitoring System
https://cmsoms.cern.ch/cms/runs/report
"""
import math

import cernrequests
from cernrequests import get_sso_cookies

from wbmcrawlr.utils import flatten_run, print_progress

OMS_API_URL = "https://cmsoms.cern.ch/agg/api/v1/"
PAGE_SIZE = 100

fields = [
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

fields_string = ",".join(fields)


# delivered_lumi = Run Lumi
# recorded_lumi = Run Live Lumi


def get_run(run_number):
    parameters = (
        "fields={fields}" "&filter[run_number][EQ]={run_number}" "&sort=-run_number"
    ).format(fields=fields_string, run_number=run_number)

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
        "fields={fields}"
        "&page[offset]={page}&page[limit]={page_size}&"
        "&filter[run_number][GE]={begin}"
        "&filter[run_number][LE]={end}"
        "&filter[sequence][EQ]=GLOBAL-RUN"
        "&sort=run_number"
    ).format(
        begin=begin,
        end=end,
        fields=fields_string,
        page=page * PAGE_SIZE,
        page_size=PAGE_SIZE,
    )

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
