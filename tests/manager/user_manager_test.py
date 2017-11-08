#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.config.credentials import Credentials

from scs_philips_hue.manager.upnp_discovery import UPnPDiscovery
from scs_philips_hue.manager.user_manager import UserManager


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

user_manager = UserManager(HTTPClient(), bridge.ip_address, credentials.username)
print(user_manager)

print("-")

entries = user_manager.find_all()

for entry in entries:
    print(entry)

print("-")

entry = user_manager.find(credentials.username)
print(entry)
