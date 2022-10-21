#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

_rootdir = os.path.dirname(os.path.realpath(__file__))
_hadir = "{}/lib/ha".format(_rootdir)
_libdir = "{}/lib".format(_rootdir)

sys.path.append(_rootdir)
sys.path.append(_libdir)
sys.path.append(_hadir)

try:
    import paho.mqtt.publish as publish
    import yaml
    import json
except Exception as e:
    print('Import error {}, check requirements.txt'.format(e))

try:
    from lib import utils
    import config.app_config as app_config
    from lib import logger

except Exception as e:
    print('Application {} Configuration error {}, check settings.py'.format(__name__, e))
    sys.exit(1)


# register the application logger
log = logger.Log(__name__, app_config.LOGGER_LEVEL)


class haDiscoveryItems():
    """ generate homeassistant mqtt discovery items"""

    def __init__(self, config):
        """constructor haDiscoveryItems"""
        self.cd = config
        self.brand = config["brand"]

        log.setLoglevel(level=app_config.LOGGER_LEVEL)

    def publish(self) -> int:
        """publish all ha discovery items for the gasmeter values based on the configuration settings"""
        try:

            # optional attributtes
            attr = ["ic", "device_class", "unit_of_meas", "state_class", "payload_on", "payload_off", "ent_cat", "sa", "command_topic"]
            intCounter = 1

            if os.path.isfile(self.cd['ha_schema']) and os.path.isfile(self.cd['ha_items']):

                # valid setting found, open the file
                data = utils.loadYaml(self.cd['ha_items'])
                payloads = utils.loadYaml(self.cd['ha_schema'])

                if data is None or payloads is None:
                    log.debug("{}: No data found for files {}, {}".format(sys._getframe().f_code.co_name, self.cd['ha_schema'], self.cd['ha_items']))
                    return intCounter - 1

                log.debug("{}: Loaded files {}, {}".format(sys._getframe().f_code.co_name, self.cd['ha_schema'], self.cd['ha_items']))

                items = data["items"]

                # interate throw all entities
                for item in items:

                    if (int(item["enabled"] == 1)):

                        if "schema" in item:

                            itemType = item["type"]

                            # update the fields
                            payload = payloads[item["schema"]]

                            # GUI Name and entity id's
                            name = "{} {}".format(self.cd["brand"], item["name"])
                            payload["name"] = name

                            uniq_id = ("{}.{}".format(self.cd["deviceid"], item["field"], item["field"])).replace("-","_")
                            payload["uniq_id"] = uniq_id.replace(".","_")

                            payload["object_id"] = "{}_{}".format(self.cd["brandname"], uniq_id)

                            val_tpl = "{{{{value_json.{}}}}}".format(item["field"])
                            if "val_tpl" in item:
                                val_tpl = item["val_tpl"]                                
                            payload["val_tpl"] = val_tpl

                            if "json_attr_t" in item:
                                payload["json_attr_t"] = item["json_attr_t"]

                            if "~" in item:
                                payload["~"] = item["~"]

                            if "stat_t" in item:
                                payload["stat_t"] = item["stat_t"]

                            if "ent_cat" in item:
                                payload["ent_cat"] = item["ent_cat"]

                            # update | remove emty optional attributes
                            for tag in attr:
                                if tag in item:
                                    payload[tag] = item[tag]
                                else:
                                    if tag in payload:
                                        del payload[tag]

                            # TODO: remove all empty or null items

                            # set the tpoic name
                            topic_name = "{}".format(item["field"].replace(".", "_").lower())
                            
                            if "discovery_prefix" in self.cd:
                                # publish item
                                topic = "{}/{}/{}/{}/config".format(self.cd["discovery_prefix"], itemType, self.cd["deviceid"], topic_name)
                                # mqtt brocker defined, send Topic
                                if app_config.HA_DISCOVERY_MODE == 'developer':
                                    log.debug("Publish discovery item:{}, {}".format(topic_name, topic))
                                if app_config.MQTT_HOST:                                        
                                    publish.single(topic,
                                                payload=json.dumps(payload, ensure_ascii=False),
                                                retain=True,
                                                hostname=app_config.MQTT_HOST,
                                                port=app_config.MQTT_PORT,
                                                client_id=app_config.MQTT_CLIENTID,
                                                keepalive=60,
                                                auth=app_config.MQTT_AUTH)

                            # save the payload for checking
                            if app_config.HA_DISCOVERY_MODE == 'developer':
                                path = "{}ha/{}/{}".format(app_config.DATADIR, self.cd["brandname"], itemType)
                                if not os.path.exists(path):
                                    os.makedirs(path)
                                ha_file = "{}/{}-{}.json".format(path, intCounter, topic_name)
                                log.debug("Save ha-discovery item:{}".format(ha_file))
                                with open(ha_file, 'w', encoding='utf-8') as f:
                                    json.dump(payload, f, indent=4, ensure_ascii=False)

                            intCounter += 1

            return intCounter - 1

        except BaseException as e:
            log.error(f"Error {sys._getframe().f_code.co_name}, {str(e)}, {str(e)} line {sys.exc_info()[-1].tb_lineno}")
            return False
