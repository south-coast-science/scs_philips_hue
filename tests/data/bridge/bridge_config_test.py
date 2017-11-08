#!/usr/bin/env python3

"""
Created on 28 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.data.json import JSONify

from scs_philips_hue.data.bridge.bridge_config import BridgeConfig

# --------------------------------------------------------------------------------------------------------------------

jstr = '{' \
       '"name": "scs-hb-001", ' \
       '"zigbeechannel": 20, ' \
       '"bridgeid": "001788FFFE795620", ' \
       '"mac": "00:17:88:79:56:20", ' \
       '"dhcp": true, ' \
       '"ipaddress": "192.168.1.10", ' \
       '"netmask": "255.255.255.0", ' \
       '"gateway": "192.168.1.1", ' \
       '"proxyaddress": "none", ' \
       '"proxyport": 0, ' \
       '"UTC": "2017-10-28T14:16:10", ' \
       '"localtime": "2017-10-28T15:16:10", ' \
       '"timezone": "Europe/London", ' \
       '"modelid": "BSB002", ' \
       '"datastoreversion": "63", ' \
       '"swversion": "1709131301", ' \
       '"apiversion": "1.21.0", ' \
       '"swupdate": {' \
       '"updatestate": 0, ' \
       '"checkforupdate": false, ' \
       '"devicetypes": {"bridge": false, "lights": [], "sensors": []}, ' \
       '"url": "", ' \
       '"text": "", ' \
       '"notify": false}, ' \
       '"swupdate2": {' \
       '"checkforupdate": false, ' \
       '"lastchange": "2017-10-27T15:10:38", ' \
       '"bridge": {"state": "noupdates", "lastinstall": null}, ' \
       '"state": "noupdates", ' \
       '"autoinstall": {"updatetime": "T14:00:00", "on": false}}, ' \
       '"linkbutton": false, ' \
       '"portalservices": true, ' \
       '"portalconnection": "connected", ' \
       '"portalstate": {"signedon": true, "incoming": false, "outgoing": true, "communication": "disconnected"}, ' \
       '"internetservices": {"internet": "connected", "remoteaccess": "connected", "time": "connected", ' \
       '"swupdate": "connected"}, ' \
       '"factorynew": false, ' \
       '"replacesbridgeid": null, ' \
       '"backup": {"status": "idle", "errorcode": 0}, ' \
       '"starterkitid": "", ' \
       '"whitelist": {' \
       '"kakoh96DKsic6XGC9-v07nVIUig1naMOgv849i1r": {' \
       '"last use date": "2017-10-27T20:02:32", "create date": "2017-10-27T15:04:55", "name": "scs_hue#bruno"}, ' \
       '"11uK-QDNOytTk7UW6smCBYBVZXxKaFy3b72b7Qdv": {' \
       '"last use date": "2017-10-27T15:17:32", "create date": "2017-10-27T15:10:10", "name": "Hue 2#HTC U11"}, ' \
       '"b8bvymOH-ceugK8gBOpjeNeL0OMhXOEBQZosfsTx": {' \
       '"last use date": "2017-10-28T14:16:10", "create date": "2017-10-27T20:48:42", "name": "scs_hue#bruno"}}}'
print(jstr)
print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
print(jdict)
print("-")

config = BridgeConfig.construct_from_jdict(jdict)
print(config)
print("-")

print(JSONify.dumps(config.as_json()))
