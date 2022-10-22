#!/usr/bin/env python3
# -*- coding':' utf-8 -*-

# ----------------------------------------------
# Contact Bosh-Siemens Home Connect devices
# and connect their messages to the mqtt server
# ----------------------------------------------

import os
import sys
import string

_rootdir = os.path.dirname(os.path.realpath(__file__))
_hcdir = "{}/lib/hc".format(_rootdir)
_hadir = "{}/lib/ha".format(_rootdir)
_libdir = "{}/lib".format(_rootdir)

sys.path.append(_rootdir)
sys.path.append(_libdir)
sys.path.append(_hcdir)
sys.path.append(_hadir)

try:
    import json
    import re
    import time
    import io
    import paho.mqtt.publish as publish
    import threading

except Exception as e:
    print('Import error {}, check requirements.txt'.format(e))

try:
    from hc.socket import HCSocket, now
    from hc.device import HCDevice
    from ha.ha_discoveryitems import *
    from lib import utils
    import config.app_config as app_config
    from lib import logger

except Exception as e:
    print('Application {} Configuration error {}, check settings.py'.format(__name__, e))
    sys.exit(1)

log = logger.Log(__name__, app_config.LOGGER_LEVEL)


def __calcRunningTime__(sdat):
    """ internal helper method to calc the running time """

    try:
        d1 = utils.strToDate(sdat, "%Y-%m-%d %H:%M:%S")
        d2 = utils.now()
        if d1:
            return (utils.runningTime((d2 - d1).total_seconds()))

    except BaseException as e:
        log.error(f"{__name__}: FATAL ERROR Heartbeat   - {str(e)}, line {sys.exc_info()[-1].tb_lineno}")

    return ""


def __saveData__(tag, data) -> bool:
    """ save the data to the filename based on the tag """

    log.info("Save Data")
    try:
        return True
    except BaseException as e:
        log.error(f"{__name__}: FATAL ERROR Heartbeat   - {str(e)}, line {sys.exc_info()[-1].tb_lineno}")

    return False


def __save2HistoryData__(data) -> bool:
    """ save the data to the history file based on the """

    try:
        if "brand" in data:
            _filename = "{}".format(app_config.DATA, data["brand"])
            log.info("Save History data")
            return True
    except BaseException as e:
        log.error(f"{__name__}: FATAL ERROR Heartbeat   - {str(e)}, line {sys.exc_info()[-1].tb_lineno}")

    return False


def publishHeartBeat(device) -> bool:
    """publish the heart beat for the defined device"""

    try:

        if not app_config.MQTT_HOST:
            log.debug("Mqtt not enabled, skipping...")
            return True

        if device:
            log.debug("Start Publish Heartbeat for {}".format(device['brand']))
            while True:
                if "config" in device and "name" in device:
                    _settings = device["config"]
                    _payload = json.dumps({
                        "state": "on",
                        "device": device['name'],
                        "uptime": __calcRunningTime__(app_config.APPS_START_TIME),
                        "totalrunning": __calcRunningTime__(_settings['installed']),
                        "tabs": _settings['taps'],
                        "tabsmin": _settings['taps_min'],
                        "timestamp": app_config.getDate(),
                        "dataprovider": os.uname().nodename,
                        "attribution": app_config.ATTRIBUTION
                    })
                    if "brand" in device:
                        _brandname = (device['brand']).lower()
                        _topic = "{}/{}-{}/heartbeat".format(app_config.MQTT_TOPIC_BASE, _brandname, device["name"])
                        log.debug("Publish Heartbeat {}".format(_topic))
                        publish.single(_topic,
                                       payload=_payload,
                                       qos=0,
                                       retain=False,
                                       hostname=app_config.MQTT_HOST,
                                       port=app_config.MQTT_PORT,
                                       client_id=app_config.MQTT_CLIENTID,
                                       keepalive=60,
                                       auth=app_config.MQTT_AUTH)
                    else:
                        log.warning("Heartbeat failed, because no brand found !")
                    time.sleep(30)
                else:
                    log.warning("Config or name not present in device config !")

            return True

    except BaseException as e:
        log.error(f"{__name__}: FATAL ERROR Heartbeat   - {str(e)}, line {sys.exc_info()[-1].tb_lineno}")
        return False


def __calcTabsOrder__(config) -> str:
    """ calculates the tabs """

    return ""


def client_connect(device) -> bool:
    """ connect the the defined device and publish the data. """

    if not device:
        log.warning("No device found !")
        return False

    if ("name" in device) and ("config" in device):

        state = {}
        _devicename = device['name']
        _device_config = device['config']
        _hostname = device['host']

        if not "brand" in device:
            log.warning("Missing brand in device {} !".format(_devicename))

        _brandname = (device['brand']).lower()

        if _device_config["hostname"]:
            _hostname = _device_config["hostname"]

        _debugMode = False
        if app_config.APPS_MODE == "developer":
            _debugMode = True

        topics = _device_config["topics"]

        for topic in topics:
            state[topics[topic]] = None

        while True:

            try:

                log.info("Connect to device: {}, Key: {} ".format(_hostname, device["key"]))

                ws = HCSocket(_hostname, device["key"], device.get("iv", None))
                dev = HCDevice(ws, device.get("features", None))
                ws.debug = False
                if _debugMode:
                    ws.debug = _debugMode

                ws.reconnect()

                while True:

                    msg = dev.recv()

                    if msg is None:
                        break

                    if len(msg) > 0:
                        log.debug("Message o.k {} ".format(_hostname))

                    if app_config.MQTT_HOST and _debugMode:
                        _topic = "{}/{}-{}/message".format(app_config.MQTT_TOPIC_BASE, _brandname, _devicename)
                        _payload = json.dumps(msg)
                        log.debug("Publish new message data to topic {} ".format(_topic))
                        publish.single(_topic,
                                       payload=_payload,
                                       qos=0,
                                       retain=True,
                                       hostname=app_config.MQTT_HOST,
                                       port=app_config.MQTT_PORT,
                                       client_id=app_config.MQTT_CLIENTID,
                                       keepalive=60,
                                       auth=app_config.MQTT_AUTH)

                    update = False
                    for topic in topics:
                        value = msg.get(topic, None)
                        if value is None:
                            log.debug("No value found for topic: {}".format(topic))
                            continue
                        # mapping incomming topic value to configuration mapped topic
                        new_topic = topics[topic]
                        if new_topic == "remaining":
                            state["remainingseconds"] = value
                            value = "%d:%02d" % (value / 60 / 60, (value / 60) % 60)
                        # set the new value for the topic
                        state[new_topic] = value
                        update = True

                    if not update:
                        continue

                    # new topic value present, so we can do the rest
                    if ("taps" in _device_config) and ("taps_min" in _device_config):
                        # calc the taps (optional)
                        state["tapscounter"] = 1
                        state["tapsorder"] = __calcTabsOrder__({"state": state, "taps": _device_config["taps"], "taps_min": _device_config["taps_min"]})

                    # add device additional attributes
                    state["device"] = device["host"]
                    state["lastupdate"] = app_config.getDate()
                    state["dataprovider"] = os.uname().nodename
                    state["attribution"] = app_config.ATTRIBUTION

                    if app_config.MQTT_HOST:
                        _topic = "{}/{}-{}/status".format(app_config.MQTT_TOPIC_BASE, _brandname, _devicename)
                        _payload = json.dumps(state)
                        log.debug("Publish new data to topic {} ".format(_topic))
                        publish.single(_topic,
                                       payload=_payload,
                                       qos=0,
                                       retain=True,
                                       hostname=app_config.MQTT_HOST,
                                       port=app_config.MQTT_PORT,
                                       client_id=app_config.MQTT_CLIENTID,
                                       keepalive=60,
                                       auth=app_config.MQTT_AUTH)
                    else:
                        # just for testcase, log the payload to the console
                        log.debug("Mqtt disabled, skip publish to mqtt.")
                        log.debug("Payload Data: {}".format(state))

            except Exception as e:
                log.error(f"{__name__}: connect Error: {str(e)}, line {sys.exc_info()[-1].tb_lineno}")
                time.sleep(20)
    else:
        log.warning(f"{__name__}: No device name or config found! - {str(e)}, line {sys.exc_info()[-1].tb_lineno}")


def publishHADiscovery(brand, device) -> bool:
    """ publish the ha discover service """
    try:

        # simple file check
        if (not os.path.isfile(device["ha_schema"])) or (not os.path.isfile(device["ha_items"])):
            log.debug("No HA-Discovery configuration present")
        else:
            log.info("HA Discovery for :".format(brand))
            hadis = haDiscoveryItems(device)
            n = hadis.publish()
        return True

    except Exception as e:
        log.error(f"{__name__}: connect Error: {str(e)}, line {sys.exc_info()[-1].tb_lineno}")

    return True


def runMqttService(brand) -> bool:
    """
      run mqtt service for the selected band. Executes the ha discovery and runs the
      mqtt heartbeat- and dataserver.
    """

    log.setLoglevel(level=app_config.LOGGER_LEVEL)
    app_config.APPS_START_TIME = app_config.getDate()
    _filename = "{}{}/{}".format(app_config.CONIG_DIR, brand, app_config.DEVICES_FILENAME)

    if not os.path.isfile(_filename):
        log.info("config file {} present. Skip get config from cloud!".format(_filename))
        return True
    else:
        log.info("Start Thread Data service, loading brand configuration file")
        devices = utils.loadjsondata(_filename)
        for device in devices:
            if publishHADiscovery(brand, device):
                log.info("Finished HA Discovery for {}".format(brand))
                time.sleep(1)
                log.info("Start get data from device: {}".format(device['host']))
                t1 = threading.Thread(target=client_connect, args=(device,))
                t1.start()
                if app_config.MQTT_HOST:
                    log.info("Publish LWT State for {} {}".format(brand, device["name"]))
                    _topic = "{}/{}-{}/LWT".format(app_config.MQTT_TOPIC_BASE, brand, device["name"])
                    log.debug("Publish LWT Topic ONLINE: {}".format(_topic))
                    publish.single(_topic,
                                   payload="online",
                                   qos=0,
                                   retain=True,
                                   hostname=app_config.MQTT_HOST,
                                   port=app_config.MQTT_PORT,
                                   client_id=app_config.MQTT_CLIENTID,
                                   keepalive=60,
                                   auth=app_config.MQTT_AUTH)
                time.sleep(.5)
                t2 = threading.Thread(target=publishHeartBeat, args=(device,))
                t2.start()

        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            pass
        finally:
            log.info("Send LWT for {} devices".format(brand))

        if _topic and app_config.MQTT_HOST:
            log.info("Publish LWT Topic OFFLINE: {}".format(_topic))
            publish.single(_topic,
                           payload="offline",
                           qos=0,
                           retain=True,
                           hostname=app_config.MQTT_HOST,
                           port=app_config.MQTT_PORT,
                           client_id=app_config.MQTT_CLIENTID,
                           keepalive=60,
                           auth=app_config.MQTT_AUTH)

    log.info("data2Mqtt is offline")
