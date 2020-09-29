#!/usr/bin/env python3

"""
Created on 27 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_philips_hue.client.upnp_client import UPnPClient


# --------------------------------------------------------------------------------------------------------------------

client = UPnPClient()
print(client)

try:
    client.connect()
    descriptions = client.get()

    for description in descriptions:
        print(description)

finally:
    client.close()

