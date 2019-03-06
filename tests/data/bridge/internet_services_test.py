#!/usr/bin/env python3

"""
Created on 28 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify

from scs_philips_hue.data.bridge.internet_services import InternetServices


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"internet": "connected1", "remoteaccess": "connected2", "time": "connected3", "swupdate": "connected4"}'
print(jstr)

print("-")

jdict = json.loads(jstr)
print(jdict)

services = InternetServices.construct_from_jdict(jdict)
print(services)

print("-")

print(JSONify.dumps(services.as_json()))
