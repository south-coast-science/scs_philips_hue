#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_philips_hue.config.bridge_credentials import BridgeCredentials


# --------------------------------------------------------------------------------------------------------------------

bridge_id = "001788fffe795620"
username = "b8bvymOH-ceugK8gBOpjeNeL0OMhXOEBQZosfsTx"

credentials = BridgeCredentials(bridge_id, username)

print("build...")
print(credentials)
print("-")

print("JSON...")
print(JSONify.dumps(credentials))
print("-")

print("save...")
credentials.save(Host)
print("-")

credentials = BridgeCredentials.load(Host)

print("load...")
print(credentials)
print("-")
