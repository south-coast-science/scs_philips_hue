#!/usr/bin/env python3

"""
Created on 28 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify

from scs_philips_hue.data.light.light_state import LightState


# --------------------------------------------------------------------------------------------------------------------

jstr = '{' \
       '"on": true, ' \
       '"bri": 254, ' \
       '"hue": 8418, ' \
       '"sat": 140, ' \
       '"effect": "none", ' \
       '"xy": [0.4573, 0.41], ' \
       '"ct": 366, ' \
       '"alert": "select", ' \
       '"colormode": "ct", ' \
       '"reachable": true}'
print(jstr)

print("-")

jdict = json.loads(jstr)
print(jdict)

print("-")

state = LightState.construct_from_jdict(jdict)
print(state)

print("-")

print(JSONify.dumps(state.as_json()))
