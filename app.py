#!/usr/bin/python3
# -*- coding":" utf-8 -*-

# ------------------------------------------------------------------
# Dataprovider for all smarthome devices
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
# @call:  python3 app.py -l INFO
#
# ------------------------------------------------------------------

import os
import sys

_rootdir = os.path.dirname(os.path.realpath(__file__))
_hcdir = "{}/lib/hc".format(_rootdir)
_libdir = "{}/lib".format(_rootdir)

sys.path.append(_rootdir)
sys.path.append(_libdir)
sys.path.append(_hcdir)


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
    # hc service
    import lib.hc.login as hclogin
    import lib.hc.data2mqtt as hcdata

except Exception as e:
    print('Application Configuration error {}, check settings.py'.format(e))
    sys.exit(1)


"""the application logger"""
log = logger.Log(__name__)


def setLogger(args: list = "Info"):
    """ set logger based on the arguments"""
    if args:
        logging_argparse = argparse.ArgumentParser(prog=__file__, add_help=False)
        logging_argparse.add_argument('-l', '--log-level', default='NONE', help='set log level')
        logging_args, _ = logging_argparse.parse_known_args(args)
        app_config.LOGGER_LEVEL_SET = logging_args.log_level
        try:
            if not logging_args.log_level in log.LOGLEVELMAP or logging_args.log_level == "NONE":
                log.loglevel = log.LOGLEVELMAP["NOLOG"]
                log.setLoglevel(level=log.LOGLEVELMAP["NOLOG"])
            else:
                log.loglevel = log.LOGLEVELMAP[logging_args.log_level]
                log.setLoglevel(level=log.LOGLEVELMAP[logging_args.log_level])

            app_config.LOGGER_LEVEL = log.loglevel
            #print("New Loglevel", app_config.LOGGER_LEVEL_SET, logging_args.log_level, app_config.LOGGER_LEVEL)
            log.info("Current Logger Loglevel:{}".format(app_config.LOGGER_LEVEL))

        except ValueError:
            log.error("Invalid log level: {}".format(logging_args.log_level))
            sys.exit(1)


if __name__ == '__main__':
    """Start Main application"""
    try:
        # start  and set the application parameters 
        setLogger(sys.argv[1:])
        log.info("Application is running")
        app_config.APPS_START_TIME = app_config.getDate()

        # current only for bosch...
        # TODO: add logic for more brand's
        _brandname = "bosch"
        devicelist = app_config.DEVICES[_brandname]
        if devicelist:
            # login th the brand cloud to get the device data
            if hclogin.getConfig(_brandname, devicelist):
                log.info("Config loaded and ready for brand: {}".format(_brandname))
                # now run the mqtt services for the selected device
                hcdata.runMqttService(_brandname)

    except KeyboardInterrupt:
        pass
    except BaseException as e:
        log.error(f"{__name__}: FATAL APP   - {str(e)}, line {sys.exc_info()[-1].tb_lineno}")
    finally:
        log.info("Main Program end")
