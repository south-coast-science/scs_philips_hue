#!/usr/bin/env python3

"""
Created on 4 Mar 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.discovery.ip_discovery import IPDiscovery


# --------------------------------------------------------------------------------------------------------------------
# run...

discovery = IPDiscovery(Host, HTTPClient())
print("discovery: %s" % discovery)
print("-")

start_time = time.time()

bridge = discovery.find_first()

print("bridge: %s" % bridge)
print("-")

elapsed_time = time.time() - start_time
print("elapsed: %0.3f" % elapsed_time)
