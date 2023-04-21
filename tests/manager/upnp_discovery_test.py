#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host

from scs_philips_hue.config.bridge_credentials import BridgeCredentialsSet

from scs_philips_hue.discovery.discovery import Discovery


# --------------------------------------------------------------------------------------------------------------------

credentials_set = BridgeCredentialsSet.load(Host)
print(credentials_set)

credentials = credentials_set.credentials('hue-br1-001')
print(credentials)

print("-")

discovery = Discovery(Host)
print("discovery: %s" % discovery)

print("-")

bridges = discovery.find_all()

for bridge in bridges:
    print("bridge: %s" % bridge)

print("-")

bridge = discovery.find(credentials)
print("found: %s" % bridge)

