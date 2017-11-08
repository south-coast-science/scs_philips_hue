#!/usr/bin/env python3

"""
Created on 28 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.data.json import JSONify

from scs_philips_hue.data.bridge.whitelist import WhitelistGroup


# --------------------------------------------------------------------------------------------------------------------

jstr = '{' \
        '"kakoh96DKsic6XGC9-v07nVIUig1naMOgv849i1r": ' \
        '{"last use date": "2017-10-27T20:02:32", "create date": "2017-10-27T15:04:55", "name": "scs_hue#bruno"}, ' \
        '"11uK-QDNOytTk7UW6smCBYBVZXxKaFy3b72b7Qdv": ' \
        '{"last use date": "2017-10-27T15:17:32", "create date": "2017-10-27T15:10:10", "name": "Hue 2#HTC U11"}, ' \
        '"b8bvymOH-ceugK8gBOpjeNeL0OMhXOEBQZosfsTx": ' \
        '{"last use date": "2017-10-27T23:21:27", "create date": "2017-10-27T20:48:42", "name": "scs_hue#bruno"}}'

print(jstr)

print("-")

jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
print(jdict)

group = WhitelistGroup.construct_from_jdict(jdict)
print(group)

print("-")

print(JSONify.dumps(group.as_json()))
