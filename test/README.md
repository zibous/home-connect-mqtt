# Simple Testcases

This section holds simple testcases for:

  - Login Home Connect appliances to get the devices settings
  - Homeassistant MQTT Discovery Service
  - Testcase MQTT for the registrated Devices


## Testcase Authenticate to the cloud servers

The hc-login script perfoms the OAuth process to login to your Home Connect account with your usename and password. 

```bash
 ⚡ > cd /app/home-connect-mqtt/test
 ⚡ > python3 ha-login.py
```

### Result:
It receives a bearer token that can then be used to retrieves a list of all the connected devices, their authentication and encryption keys, and XML files that describe all of the features and options.

Creates the `config/devices.json` and the `config/{brand}/{maschine}/maschine.json` for all registrated devices.

```log
2022/10/21 13:16:26.059  - INFO: Start hc login app
2022/10/21 13:16:26.060  - INFO: hc login getConfig startet
2022/10/21 13:16:26.060  - DEBUG: Testcase enabled, try to get the devices data
2022/10/21 13:16:26.060  - INFO: Get Device configuration from Bosch Cloud
....
2022/10/21 13:16:27.598  - DEBUG: Save account data to:/app/home-connect-mqtt/config//bosch/account.json
2022/10/21 13:16:27.598  - INFO: fetching: https://prod.reu.rest.homeconnectegw.com/api/iddf/v1/iddf/012090517380017161
2022/10/21 13:16:27.895  - DEBUG: Save account data to:/app/home-connect-mqtt/config/bosch/dishwasher/machine.json
2022/10/21 13:16:27.897  - INFO: Save new Config saved:/app/home-connect-mqtt/config/bosch/devices.json
2022/10/21 13:16:27.897  - INFO: Config loaded and ready for brand: bosch
```

This only needs to be done once or when you add new devices; the resulting configuration JSON file should be sufficient to connect to the devices on your local network, assuming that your mDNS or DNS server resolves the names correctly.

<br>

## Testcase Home Connect to HA Disccovery

```bash
 ⚡ > cd /app/home-connect-mqtt/test
 ⚡ > python3 ha-discovery.py
```

```log
2022/10/21 13:10:49.242  - INFO: Start ha discovery app
2022/10/21 13:10:49.243  - INFO: Start ha discovery for bosch devices
2022/10/21 13:10:49.285  - DEBUG: publish: Loaded files /app/home-connect-mqtt/config/bosch/dishwasher/schemalist.yaml, /app/home-connect-mqtt/config/bosch/dishwasher/discovery.yaml
2022/10/21 13:10:49.285  - DEBUG: Publish discovery item:power, homeassistant/binary_sensor/bosch-dishwasher/power/config
2022/10/21 13:10:49.288  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/1-power.json
2022/10/21 13:10:49.289  - DEBUG: Publish discovery item:door, homeassistant/binary_sensor/bosch-dishwasher/door/config
2022/10/21 13:10:49.292  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/2-door.json
2022/10/21 13:10:49.292  - DEBUG: Publish discovery item:waterleak, homeassistant/binary_sensor/bosch-dishwasher/waterleak/config
2022/10/21 13:10:49.296  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/3-waterleak.json
2022/10/21 13:10:49.297  - DEBUG: Publish discovery item:lowwater, homeassistant/binary_sensor/bosch-dishwasher/lowwater/config
2022/10/21 13:10:49.301  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/4-lowwater.json
2022/10/21 13:10:49.302  - DEBUG: Publish discovery item:error, homeassistant/binary_sensor/bosch-dishwasher/error/config
2022/10/21 13:10:49.304  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/5-error.json
2022/10/21 13:10:49.305  - DEBUG: Publish discovery item:halfload, homeassistant/binary_sensor/bosch-dishwasher/halfload/config
2022/10/21 13:10:49.308  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/6-halfload.json
2022/10/21 13:10:49.309  - DEBUG: Publish discovery item:programend, homeassistant/binary_sensor/bosch-dishwasher/programend/config
2022/10/21 13:10:49.311  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/7-programend.json
2022/10/21 13:10:49.312  - DEBUG: Publish discovery item:checkfilter, homeassistant/binary_sensor/bosch-dishwasher/checkfilter/config
2022/10/21 13:10:49.314  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/8-checkfilter.json
2022/10/21 13:10:49.315  - DEBUG: Publish discovery item:state, homeassistant/sensor/bosch-dishwasher/state/config
2022/10/21 13:10:49.319  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/9-state.json
2022/10/21 13:10:49.319  - DEBUG: Publish discovery item:programm, homeassistant/sensor/bosch-dishwasher/programm/config
2022/10/21 13:10:49.322  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/10-programm.json
2022/10/21 13:10:49.323  - DEBUG: Publish discovery item:remaining, homeassistant/sensor/bosch-dishwasher/remaining/config
2022/10/21 13:10:49.325  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/11-remaining.json
2022/10/21 13:10:49.326  - DEBUG: Publish discovery item:progress, homeassistant/sensor/bosch-dishwasher/progress/config
2022/10/21 13:10:49.329  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/12-progress.json
2022/10/21 13:10:49.329  - DEBUG: Publish discovery item:lastupdate, homeassistant/sensor/bosch-dishwasher/lastupdate/config
2022/10/21 13:10:49.332  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/13-lastupdate.json
2022/10/21 13:10:49.333  - DEBUG: Publish discovery item:device, homeassistant/sensor/bosch-dishwasher/device/config
2022/10/21 13:10:49.335  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/14-device.json
2022/10/21 13:10:49.336  - DEBUG: Publish discovery item:uptime, homeassistant/sensor/bosch-dishwasher/uptime/config
2022/10/21 13:10:49.341  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/15-uptime.json
2022/10/21 13:10:49.341  - DEBUG: Publish discovery item:totalrunning, homeassistant/sensor/bosch-dishwasher/totalrunning/config
2022/10/21 13:10:49.344  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/16-totalrunning.json
2022/10/21 13:10:49.345  - DEBUG: Publish discovery item:heartbeattime, homeassistant/sensor/bosch-dishwasher/heartbeattime/config
2022/10/21 13:10:49.347  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/17-heartbeattime.json
2022/10/21 13:10:49.348  - INFO: End ha discovery
```

### Result:

![HA Discovery Data](../doc/mqtt_ha_discovery.png)

## Testcase Home Connect to MQTT

This tool will establish websockets to the local devices and transform their messages into MQTT JSON messages. 

```bash
 ⚡ > cd /app/home-connect-mqtt/test
 ⚡ > python3 ha-mqtt.py
```

```log
2022/10/21 13:18:04.365  - INFO: Start hc login app
2022/10/21 13:18:04.365  - INFO: Start Thread Data service, loading brand configuration file
2022/10/21 13:18:04.365  - INFO: HA Discovery for :
2022/10/21 13:18:04.407  - DEBUG: publish: Loaded files /app/home-connect-mqtt/config/bosch/dishwasher/schemalist.yaml, /app/home-connect-mqtt/config/bosch/dishwasher/discovery.yaml
2022/10/21 13:18:04.407  - DEBUG: Publish discovery item:power, homeassistant/binary_sensor/bosch-dishwasher/power/config
2022/10/21 13:18:04.412  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/1-power.json
2022/10/21 13:18:04.413  - DEBUG: Publish discovery item:door, homeassistant/binary_sensor/bosch-dishwasher/door/config
2022/10/21 13:18:04.418  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/2-door.json
2022/10/21 13:18:04.418  - DEBUG: Publish discovery item:waterleak, homeassistant/binary_sensor/bosch-dishwasher/waterleak/config
2022/10/21 13:18:04.424  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/3-waterleak.json
2022/10/21 13:18:04.424  - DEBUG: Publish discovery item:lowwater, homeassistant/binary_sensor/bosch-dishwasher/lowwater/config
2022/10/21 13:18:04.429  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/4-lowwater.json
2022/10/21 13:18:04.429  - DEBUG: Publish discovery item:error, homeassistant/binary_sensor/bosch-dishwasher/error/config
2022/10/21 13:18:04.434  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/5-error.json
2022/10/21 13:18:04.435  - DEBUG: Publish discovery item:halfload, homeassistant/binary_sensor/bosch-dishwasher/halfload/config
2022/10/21 13:18:04.439  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/6-halfload.json
2022/10/21 13:18:04.440  - DEBUG: Publish discovery item:programend, homeassistant/binary_sensor/bosch-dishwasher/programend/config
2022/10/21 13:18:04.446  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/7-programend.json
2022/10/21 13:18:04.447  - DEBUG: Publish discovery item:checkfilter, homeassistant/binary_sensor/bosch-dishwasher/checkfilter/config
2022/10/21 13:18:04.458  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/binary_sensor/8-checkfilter.json
2022/10/21 13:18:04.458  - DEBUG: Publish discovery item:state, homeassistant/sensor/bosch-dishwasher/state/config
2022/10/21 13:18:04.462  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/9-state.json
2022/10/21 13:18:04.463  - DEBUG: Publish discovery item:programm, homeassistant/sensor/bosch-dishwasher/programm/config
2022/10/21 13:18:04.470  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/10-programm.json
2022/10/21 13:18:04.470  - DEBUG: Publish discovery item:remaining, homeassistant/sensor/bosch-dishwasher/remaining/config
2022/10/21 13:18:04.475  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/11-remaining.json
2022/10/21 13:18:04.476  - DEBUG: Publish discovery item:progress, homeassistant/sensor/bosch-dishwasher/progress/config
2022/10/21 13:18:04.481  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/12-progress.json
2022/10/21 13:18:04.481  - DEBUG: Publish discovery item:lastupdate, homeassistant/sensor/bosch-dishwasher/lastupdate/config
2022/10/21 13:18:04.486  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/13-lastupdate.json
2022/10/21 13:18:04.487  - DEBUG: Publish discovery item:device, homeassistant/sensor/bosch-dishwasher/device/config
2022/10/21 13:18:04.493  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/14-device.json
2022/10/21 13:18:04.494  - DEBUG: Publish discovery item:uptime, homeassistant/sensor/bosch-dishwasher/uptime/config
2022/10/21 13:18:04.500  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/15-uptime.json
2022/10/21 13:18:04.500  - DEBUG: Publish discovery item:totalrunning, homeassistant/sensor/bosch-dishwasher/totalrunning/config
2022/10/21 13:18:04.506  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/16-totalrunning.json
2022/10/21 13:18:04.506  - DEBUG: Publish discovery item:heartbeattime, homeassistant/sensor/bosch-dishwasher/heartbeattime/config
2022/10/21 13:18:04.511  - DEBUG: Save ha-discovery item:/app/home-connect-mqtt/data/ha/bosch/sensor/17-heartbeattime.json
2022/10/21 13:18:04.511  - INFO: Finished HA Discovery for bosch
2022/10/21 13:18:05.512  - INFO: Start get data from device: BOSCH-Dishwasher-012090517380017161
2022/10/21 13:18:05.513  - INFO: Connect to device: bosch-dishwasher.siebler.home, Key: ph8qI3DtPFoaEKFPhMOb0UJv7ISZ9j8irwbKFSQm0HU
2022/10/21 13:18:05.513  - INFO: Publish LWT State for bosch dishwasher
2022/10/21 13:18:05.514  - DEBUG: Publish LWT Topic ONLINE: tele/bosch-dishwasher/LWT
2022/10/21 13:18:06.019  - DEBUG: Start Publish Heartbeat for BOSCH
2022/10/21 13:18:06.022  - DEBUG: Publish Heartbeat tele/bosch-dishwasher/heartbeat
.....
2022/10/21 13:18:07.968  - DEBUG: Message o.k bosch-dishwasher.siebler.home
2022/10/21 13:18:07.968  - DEBUG: Publish new data to topic tele/bosch-dishwasher/status
```

The exact format is likely to change; it is currently a thin translation layer over the XML retrieved from cloud servers during the initial configuration.


### Result:

Example message published to `tele/bosh/dishwasher/state`:

```json
{
	"state": "Ready",
	"door": "Closed",
	"remaining": "1:05",
	"power": "Off",
	"lowwater": "Off",
	"waterleak": "Off",
	"error": "Off",
	"programm": "None",
	"halfload": "False",
	"programend": "Off",
	"progress": "False",
	"checkfilter": "Off",
	"remainingseconds": 3900,
	"tapscounter": 1,
	"tapsorder": "",
	"device": "BOSCH-Dishwasher-012090517380017161",
	"timestamp": "2022-10-20T09:18:51",
	"dataprovider": "zeusus",
	"attribution": "Data dishwasher.service provided by Peter Siebler"
}
```

<br>
Example message published to `tele/bosh/dishwasher/heartbeat`:

```json
{
	"state": "on",
	"device": "dishwasher",
	"uptime": "14 hours, 12 minutes, 26 seconds",
	"totalrunning": "43 days, 22 hours, 54 minutes, 21 seconds",
	"tabs": 20,
	"tabsmin": 5,
	"timestamp": "2022-10-20T10:54:21",
	"dataprovider": "zeusus",
	"attribution": "Data dishwasher.service provided by Peter Siebler"
}
```
<br>
<hr>

# Acknowledgements:

+ Thanks to Trammell Hudson osresearch  https://github.com/osresearch/hcpy
