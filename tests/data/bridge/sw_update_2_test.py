#!/usr/bin/env python3

"""
Created on 28 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.data.json import JSONify

from scs_philips_hue.data.bridge.sw_update_2 import SWUpdate2


# --------------------------------------------------------------------------------------------------------------------

jstr = '{' \
       '"checkforupdate": false, ' \
       '"lastchange": "2017-10-27T15:10:38", ' \
       '"bridge": {"state": "noupdates", "lastinstall": null}, ' \
       '"state": "noupdates", ' \
       '"autoinstall": {"updatetime": "T14:00:00", "on": false}}'
print(jstr)

print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
print(jdict)

update = SWUpdate2.construct_from_jdict(jdict)
print(update)

print("-")

print(JSONify.dumps(update.as_json()))
