#!/usr/bin/env python3

"""
Created on 28 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.data.json import JSONify

from scs_philips_hue.data.bridge.portal_state import PortalState


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"signedon": true, "incoming": false, "outgoing": true, "communication": "disconnected"}'
print(jstr)

print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
print(jdict)

print("-")

state = PortalState.construct_from_jdict(jdict)
print(state)

print("-")

print(JSONify.dumps(state.as_json()))
