#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host

from scs_philips_hue.config.bridge_credentials import BridgeCredentialsSet

from scs_philips_hue.discovery.discovery import Discovery

from scs_philips_hue.manager.bridge_manager import BridgeManager


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

bridge_manager = BridgeManager(bridge.ip_address, credentials.username)
print(bridge_manager)

print("-")

config = bridge_manager.find()
print(config)

print("-")
