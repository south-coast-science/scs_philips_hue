#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_philips_hue.config.bridge_credentials import BridgeCredentials


# --------------------------------------------------------------------------------------------------------------------

bridge_name = 'hue-br1-001'
bridge_id = "001788fffe795620"
username = "b8bvymOH-ceugK8gBOpjeNeL0OMhXOEBQZosfsTx"

credentials = BridgeCredentials(bridge_name, bridge_id, username)

print("build...")
print(credentials)
print("-")

print("JSON...")
print(JSONify.dumps(credentials))
print("-")
