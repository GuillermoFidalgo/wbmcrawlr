# CMS WBM Crawler

Retrieve data from the [CMS Online Monitoring System](https://cmsoms.cern.ch/) and [CMS Web Based Monitoring](https://cmswbm.cern.ch/). Currently only the [OMS Run Summary](https://cmsoms.cern.ch/cms/runs/summary) is tool assisted.
## Installation

```bash
pip install git+https://github.com/ptrstn/wbmcrawlr
```

## Prerequisites

Setup your CERN Grid User Certificate as instructed in the cernrequests package:

- https://github.com/ptrstn/cernrequests#prerequisites

## Usage

### Help
```bash
usage: wbmcrawl [-h] min max

CERN CMS WBM and OMS crawler.

positional arguments:
  min         Minimum run number
  max         Maximum run number

optional arguments:
  -h, --help  show this help message and exit
```

### Example

To download all runs from the CMS OMS in the run number range of 313052 to 327564 do:

```bash
wbmcrawl 313052 327564
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

## References

- https://twiki.cern.ch/twiki/bin/view/CMS/WbmApi
- https://twiki.cern.ch/twiki/bin/view/CMS/OMS
- http://cmsomsapi.cern.ch:8080/api/v1/version/endpoints
- https://cmswbm.cern.ch/cmsdb/servlet/RunSummary
- https://cmsoms.cern.ch/cms/runs/summary
