#!/usr/bin/env python3

"""
Created on 28 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify

from scs_philips_hue.data.light.sw_update import SWUpdate


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"state": "noupdates", "lastinstall": null}'

print(jstr)

print("-")

jdict = json.loads(jstr)
print(jdict)

update = SWUpdate.construct_from_jdict(jdict)
print(update)

print("-")

print(JSONify.dumps(update.as_json()))
