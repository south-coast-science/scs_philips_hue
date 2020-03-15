#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.client.http_client import HTTPClient

from scs_host.sys.host import Host

from scs_philips_hue.config.bridge_credentials import BridgeCredentials

from scs_philips_hue.discovery.discovery import Discovery

from scs_philips_hue.manager.user_manager import UserManager


# --------------------------------------------------------------------------------------------------------------------

# HTTPClient...
http_client = HTTPClient(False)

credentials = BridgeCredentials.load(Host)
print(credentials)

print("-")

discovery = Discovery(Host, http_client)
print(discovery)

print("-")

bridge = discovery.find(credentials)
print(bridge)

print("=")

user_manager = UserManager(http_client, bridge.ip_address, credentials.username)
print(user_manager)

print("-")

entries = user_manager.find_all()

for entry in entries:
    print(entry)

print("-")

entry = user_manager.find(credentials.username)
print(entry)
