#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.config.credentials import Credentials

from scs_philips_hue.manager.bridge_manager import BridgeManager
from scs_philips_hue.manager.upnp_discovery import UPnPDiscovery


# --------------------------------------------------------------------------------------------------------------------

credentials = Credentials.load(Host)
print(credentials)

print("-")

upnp = UPnPDiscovery(HTTPClient())
print(upnp)

print("-")

bridge = upnp.find(credentials.bridge_id)
print(bridge)

print("=")

bridge_manager = BridgeManager(HTTPClient(), bridge.ip_address, credentials.username)
print(bridge_manager)

print("-")

config = bridge_manager.find()
print(config)

print("-")


# state = bridge_manager.get_sate()
# print(JSONify.dumps(state))
