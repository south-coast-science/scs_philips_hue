#!/usr/bin/env python3

"""
Created on 28 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
from collections import OrderedDict

from scs_core.data.json import JSONify

from scs_philips_hue.data.bridge.backup import Backup


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"status": "idle", "errorcode": 0}'
print(jstr)

print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
print(jdict)

backup = Backup.construct_from_jdict(jdict)
print(backup)

print("-")

print(JSONify.dumps(backup.as_json()))
