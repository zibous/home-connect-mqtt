
# Bosch Dishwasher

The dishwasher has a local HTTPS port open, although attempting to connect to the HTTPS port with curl results in a  cryptic protocol error due to the non-standard cipher selection, ECDHE-PSK-CHACHA20-POLY1305. 

![Bosch Geschirrspüler](../../../doc/SMV4HCX48E.png)

PSK also requires that both sides agree on a symetric key, so a special hacked version of sslpsk is used to establish the connection and then hand control to the Python websock-client library.
<br>

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
With the status topic only the messages contained in the configuration `devices.brand.serialnumber.topics` are published, this can be adjusted by further (see Full state information).


<details>
<summary>Full state information</summary>

```json
{
  "AllowBackendConnection": "false",
  "BackendConnected": "false",
  "RemoteControlLevel": "ManualRemoteStart",
  "SoftwareUpdateAvailable": "Off",
  "ConfirmPermanentRemoteStart": "Off",
  "ActiveProgram": 0,
  "SelectedProgram": 8192,
  "RemoteControlStartAllowed": "false",
  "520": "2022-02-21T16:48:54",
  "RemoteControlActive": "true",
  "AquaStopOccured": "Off",
  "DoorState": "Open",
  "PowerState": "Off",
  "ProgramFinished": "Off",
  "ProgramProgress": 100,
  "LowWaterPressure": "Off",
  "RemainingProgramTime": 0,
  "ProgramAborted": "Off",
  "547": "false",
  "RemainingProgramTimeIsEstimated": "true",
  "OperationState": "Inactive",
  "StartInRelative": 0,
  "EnergyForecast": 82,
  "WaterForecast": 70,
  "ConnectLocalWiFi": "Off",
  "SoftwareUpdateTransactionID": 0,
  "SoftwareDownloadAvailable": "Off",
  "SoftwareUpdateSuccessful": "Off",
  "ProgramPhase": "Drying",
  "SilenceOnDemandRemainingTime": 0,
  "EcoDryActive": "false",
  "RinseAid": "R04",
  "SensitivityTurbidity": "Standard",
  "ExtraDry": "false",
  "HotWater": "ColdWater",
  "TimeLight": "On",
  "EcoAsDefault": "LastProgram",
  "SoundLevelSignal": "Off",
  "SoundLevelKey": "Medium",
  "WaterHardness": "H04",
  "DryingAssistantAllPrograms": "AllPrograms",
  "SilenceOnDemandDefaultTime": 1800,
  "SpeedOnDemand": "false",
  "InternalError": "Off",
  "CheckFilterSystem": "Off",
  "DrainingNotPossible": "Off",
  "DrainPumpBlocked": "Off",
  "WaterheaterCalcified": "Off",
  "LowVoltage": "Off",
  "SaltLack": "Off",
  "RinseAidLack": "Off",
  "SaltNearlyEmpty": "Off",
  "RinseAidNearlyEmpty": "Off",
  "MachineCareReminder": "Off",
  "5121": "false",
  "HalfLoad": "false",
  "IntensivZone": "false",
  "VarioSpeedPlus": "false",
  "5131": "false",
  "5134": "true",
  "SilenceOnDemand": "false"
}
```
</details>

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