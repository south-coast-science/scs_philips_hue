#!/usr/bin/env python3

"""
Created on 30 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_philips_hue.config.bridge_credentials import BridgeCredentialsSet

from scs_philips_hue.data.light.light_state import LightState

from scs_philips_hue.discovery.discovery import Discovery

from scs_philips_hue.manager.light_manager import LightManager


# --------------------------------------------------------------------------------------------------------------------

credentials_set = BridgeCredentialsSet.load(Host)
print(credentials_set)

credentials = credentials_set.credentials('hue-br1-001')
print(credentials)

print("-")

discovery = Discovery(Host)
print(discovery)

print("-")

bridge = discovery.find(credentials)
print(bridge)

print("=")

manager = LightManager(bridge.ip_address, credentials.username)
print(manager)

print("-")

lights = manager.find_all()

for entry in lights:
    print("entry: %s" % entry)

print("-")

index = manager.find_index_for_uid("00:17:88:01:0b:b1:f5:1c-0b")
print("index: %s" % index)

print("-")

light = manager.find(index)
print(light)

print("-")

while True:
    state = LightState(bri=5)
    print(state)

    response = manager.set_state(index, state)
    print(response)

    print(JSONify.dumps(response.as_json()))

    print("-")

    time.sleep(1)

    state = LightState(bri=254)
    print(state)

    response = manager.set_state(index, state)
    print(response)

    print(JSONify.dumps(response.as_json()))

    print("=")

    time.sleep(2)

