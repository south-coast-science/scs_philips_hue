#!/usr/bin/env python3

"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host

from scs_philips_hue.config.credentials import Credentials


# --------------------------------------------------------------------------------------------------------------------

credentials = Credentials.load(Host)
print(credentials)

print("-")

credentials.bridge_id = "001788fffe795620"
credentials.username = "b8bvymOH-ceugK8gBOpjeNeL0OMhXOEBQZosfsTx"

credentials.save(Host)
print(credentials)

print("-")

credentials = Credentials.load(Host)
print(credentials)
