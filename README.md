[![Build Status](https://travis-ci.com/ptrstn/wbmcrawlr.svg?branch=master)](https://travis-ci.com/ptrstn/wbmcrawlr)

# CMS WBM Crawler

Retrieve data from the [CMS Online Monitoring System](https://cmsoms.cern.ch/) and [CMS Web Based Monitoring](https://cmswbm.cern.ch/). Currently only the [OMS Run Summary](https://cmsoms.cern.ch/cms/runs/summary) and the [OMS LHC Fill Summary](https://cmsoms.cern.ch/cms/fills/summary) is tool assisted.

## Installation

```bash
pip install git+https://github.com/ptrstn/wbmcrawlr
```

## Prerequisites

If you are not within the CERN GPN, setup your CERN Grid User Certificate as instructed in the cernrequests package:

- https://github.com/ptrstn/cernrequests#prerequisites

## Usage

### Help

```bash
usage: wbmcrawl [-h]
                (--runs min max | --fills min max | --lumisections run | --hltrates run path_name | --all-hltrates run)

CERN CMS WBM and OMS crawler.

optional arguments:
  -h, --help                show this help message and exit
  --runs min max            Retrieve Runs
  --fills min max           Retrieve Fills
  --lumisections run        Retrieve Lumisections
  --hltrates run path_name  Hlt rates for given path per lumisection
  --all-hltrates run        Hlt rates for all available paths per lumisection
```

### Example

#### Runs

To download all runs from the CMS OMS in the run number range of 313052 to 327564 do:

```bash
wbmcrawl --runs 313052 327564
```

```
Getting runs 313052 - 327564 from CMS OMS
Total number of runs: 6424

[#################---------------------------------] 33.85% Page 22/65
```

All runs will be stored in ```oms_runs.json```

```
Getting runs 313052 - 327564 from CMS OMS
Total number of runs: 6424

[##################################################] 100.00% Page 65/65

Stored 6424 runs in 'oms_runs.json'
```

#### Fills

Similarly, with the parameter ````--fills```` you get all LHC fills in the specified number range.

```bash
wbmcrawl --fills 7480 7483
```

```
Getting fills 7480 - 7483 from CMS OMS
Total number of fills: 4...

[##################################################] 100.00% Page 1/1

Stored 4 fills in 'oms_fills.json'
```

#### Lumisections

```bash
wbmcrawl --lumisections 319579
```

#### HLT Rates

```bash
wbmcrawl --hltrates 319579 HLT_AK8PFJet400_TrimMass30_v12
```

If you want all hlt rates for all possible path names you can do :

# TODO

try to acces oms api outside of cern
if inside of cern try to get without cookies
if outside do with cookies

## References

- https://twiki.cern.ch/twiki/bin/view/CMS/WbmApi
- https://twiki.cern.ch/twiki/bin/view/CMS/OMS
- http://cmsomsapi.cern.ch:8080/api/v1/version/endpoints
- https://cmswbm.cern.ch/cmsdb/servlet/RunSummary
- https://cmsoms.cern.ch/cms/runs/summary
