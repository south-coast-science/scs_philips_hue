#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host

from scs_philips_hue.config.bridge_credentials import BridgeCredentials

from scs_philips_hue.discovery.discovery import Discovery


# --------------------------------------------------------------------------------------------------------------------

credentials = BridgeCredentials.load(Host)
print("credentials: %s" % credentials)

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

