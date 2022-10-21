#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

# simple check if python 3 is used 
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

 ## all requirements
try: 
   from datetime import datetime
   import string
except Exception as e:
    print('Import error {}, check requirements.txt'.format(e))
    sys.exit(1)


# -----------------------------------------------
# date and time formats
# -----------------------------------------------
DATEFORMAT_TIMESTAMP = '%Y-%m-%dT%H:%M:%S'
DATEFORMAT_CURRENT = '%Y-%m-%d %H:%M:%S.%f'
DATEFORMAT_HOUR = '%H'
DATEFORMAT_DAY = '%Y-%m-%d'
DATEFORMAT_MONTH = '%Y-%m'
DATEFORMAT_YEAR = '%Y'
TIME_FORMAT = '%H:%M:%S'
DATEFORMAT_UTC = '%Y-%m-%dT%H:%M:%SZ'
DATE_NOW = datetime.now()
DATE_DEFAULT = DATE_NOW.strftime(DATEFORMAT_TIMESTAMP)
DATE_DEFAULT_MIN = datetime.min
now = datetime.now()
DATE_STATISTICLIST = {
   "hour": DATEFORMAT_HOUR,
   "day": DATEFORMAT_DAY,
   "month": DATEFORMAT_MONTH,
   "year": DATEFORMAT_YEAR
}

def getTimestamp() -> string:
    return datetime.now().strftime(DATEFORMAT_TIMESTAMP)