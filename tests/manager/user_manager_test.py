#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host

from scs_philips_hue.config.bridge_credentials import BridgeCredentialsSet

from scs_philips_hue.discovery.discovery import Discovery

from scs_philips_hue.manager.user_manager import UserManager


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

user_manager = UserManager(bridge.ip_address, credentials.username)
print(user_manager)

print("-")

entries = user_manager.find_all()

for entry in entries:
    print(entry)

print("-")

entry = user_manager.find(credentials.username)
print(entry)
