#!/usr/bin/python3
# -*- coding":" utf-8 -*-

# ------------------------------------------------------------------
# Testcase Dishwasher MQTT from local Network
# ------------------------------------------------------------------
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Distribution License
# which accompanies this distribution.
#
# Contributors:
#    Peter Siebler - initial implementation
#
# Copyright (c) 2022 Peter Siebler
# All rights reserved.
#
# ------------------------------------------------------------------

import os
import sys

_rootdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(_rootdir)
sys.path.append("{}/lib".format(_rootdir))
sys.path.append("{}/lib/hc".format(_rootdir))


"""
Application Docstring settings
"""
__author__ = "Peter Siebler"
__version__ = "0.1.0"
__license__ = "MIT"


"""simple check if python 3 is used"""
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    print("This script requires Python 3.5 or higher!")
    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

"""all requirements packages"""
try:
    import argparse
    import paho.mqtt.publish as publish
    import json

except Exception as e:
    print('Import error {}, check requirements.txt'.format(e))


"""all private libs"""
try:
    from lib import logger
    from lib import systools
    import config.app_config as app_config
    import lib.hc.data2mqtt as hcdata

except Exception as e:
    print('Application Configuration error {}, check settings.py'.format(e))
    sys.exit(1)


"""the application logger"""
log = logger.Log(__name__, 10)


if __name__ == '__main__':

    app_config.LOGGER_LEVEL = 10   
    log.info("Start hc login app")
    brand = "bosch"
    
    try:
        app_config.APPS_START_TIME = app_config.getDate()
        app_config.APPS_MODE = "developer"
        
        # current only for bosch...
        _brandname = "bosch"
        hcdata.runMqttService(_brandname)

    except Exception as e:
        log.error(f"{__name__}: connect Error: {str(e)}, line {sys.exc_info()[-1].tb_lineno}")
