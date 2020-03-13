#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.config.bridge_credentials import BridgeCredentials

from scs_philips_hue.discovery.discovery import Discovery


# --------------------------------------------------------------------------------------------------------------------

credentials = BridgeCredentials.load(Host)
print(credentials)

print("-")

discovery = Discovery(Host, HTTPClient(False))
print(discovery)

print("-")

bridges = discovery.find_all()

for bridge in bridges:
    print(bridge)

print("-")

bridge = discovery.find(credentials)
print(bridge)

