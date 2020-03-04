#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.config.bridge_credentials import BridgeCredentials

from scs_philips_hue.manager.bridge_manager import BridgeManager
from scs_philips_hue.manager.discovery import Discovery


# --------------------------------------------------------------------------------------------------------------------

credentials = BridgeCredentials.load(Host)
print(credentials)

print("-")

discovery = Discovery(Host, HTTPClient())
print(discovery)

print("-")

bridge = discovery.find(credentials)
print(bridge)

print("=")

bridge_manager = BridgeManager(HTTPClient(), bridge.ip_address, credentials.username)
print(bridge_manager)

print("-")

config = bridge_manager.find()
print(config)

print("-")
