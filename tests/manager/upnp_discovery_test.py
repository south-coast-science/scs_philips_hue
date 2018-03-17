#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.config.bridge_credentials import BridgeCredentials
from scs_philips_hue.manager.upnp_discovery import UPnPDiscovery


# --------------------------------------------------------------------------------------------------------------------

credentials = BridgeCredentials.load(Host)
print(credentials)

print("-")

upnp = UPnPDiscovery(HTTPClient())
print(upnp)

print("-")

bridges = upnp.find_all()

for bridge in bridges:
    print(bridge)

print("-")

bridge = upnp.find(credentials.bridge_id)
print(bridge)

