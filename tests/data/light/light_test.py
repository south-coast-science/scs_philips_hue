#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.data.json import JSONify

from scs_philips_hue.data.light.light import Light


# --------------------------------------------------------------------------------------------------------------------

jstr = '{' \
       '"state": {' \
           '"on": true, ' \
           '"bri": 254, ' \
           '"hue": 8418, ' \
           '"sat": 140, ' \
           '"effect": "none", ' \
           '"xy": [0.4573, 0.41], ' \
           '"ct": 366, ' \
           '"alert": "select", ' \
           '"colormode": "ct", ' \
           '"reachable": true' \
       '}, ' \
       '"swupdate": {"state": "noupdates", "lastinstall": null}, ' \
       '"type": "Extended color light", ' \
       '"name": "Hue color lamp 1", ' \
       '"modelid": "LCT015", ' \
       '"manufacturername": "Philips", ' \
       '"uniqueid": "00:17:88:01:03:54:25:66-0b", ' \
       '"swversion": "1.19.0_r19755", ' \
       '"swconfigid": "A724919D", ' \
       '"productid": "Philips-LCT015-1-A19ECLv5"' \
       '}'
print(jstr)

print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
print(jdict)

print("-")

light = Light.construct_from_jdict(jdict)
print(light)

print("-")

print(JSONify.dumps(light.as_json()))
