#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import paho.mqtt.publish as publish

class client:
    """MQTT Message to mqtt brocker
    """
    version = "1.0.1"

    # Constructor
    def __init__(self, host: str , port: int , clientId: str, auth):
        self.mqttBrocker = host
        self.port = port
        self.clientId = clientId
        self.auth = auth
        self.errormessage = None

    # publish data to the defined mqtt brocker
    def publish(self, payload, topic: str , qos: int = 0, retain: bool = False, keepalive: int = 60):
        try:
            if not self.mqttBrocker:
                return None
            if(self.auth):
                # publish with authenification
                publish.single(topic,
                               payload=json.dumps(payload),
                               qos=qos,
                               retain=retain,
                               hostname=self.mqttBrocker,
                               port=self.port,
                               client_id=self.clientId,
                               keepalive=keepalive,
                               auth=self.auth)
            else:
                # publish w/o authenification                
                publish.single(topic,
                               payload=json.dumps(payload),
                               qos=qos,
                               retain=retain,
                               hostname=self.mqttBrocker,
                               port=self.port,
                               client_id=self.clientId,
                               keepalive=keepalive)
        except BaseException as e:
            self.errormessage = f"{__name__} Error = {str(e)}"
            return None
