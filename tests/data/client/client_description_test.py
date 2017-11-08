#!/usr/bin/env python3

"""
Created on 27 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_philips_hue.data.client.client_description import ClientDescription


# --------------------------------------------------------------------------------------------------------------------

description = ClientDescription('scs_connector', 'bruno')
print(description)

print(JSONify.dumps(description.as_json()))
