#!/usr/bin/env python3

"""
Created on 27 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_philips_hue.client.rest_client import RESTClient


# --------------------------------------------------------------------------------------------------------------------

client = RESTClient()
print(client)

try:
    client.connect("192.168.1.10", "b8bvymOH-ceugK8gBOpjeNeL0OMhXOEBQZosfsTx")

    response = client.get("/lights")        # config    lights/1

    print(JSONify.dumps(response))

finally:
    client.close()
