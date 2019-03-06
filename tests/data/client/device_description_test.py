#!/usr/bin/env python3

"""
Created on 3 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify

from scs_philips_hue.data.client.client_description import ClientDescription
from scs_philips_hue.data.client.device_description import DeviceDescription


# --------------------------------------------------------------------------------------------------------------------

client = ClientDescription(ClientDescription.APP, 'bruno.local')
print(client)

print(JSONify.dumps(client.as_json()))

print("-")
device = DeviceDescription(client)
print(device)

print("-")
jdict = device.as_json()
print(jdict)

print("-")
jstr = JSONify.dumps(jdict)
print(jstr)

print("-")
jdict = json.loads(jstr)

device = DeviceDescription.construct_from_jdict(jdict)
print(device)
