#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"NO2": {"path-name": "risk-level", "domain-min": 0.0, "domain-max": 50.0, "brightness": 254, "transition-time": 9},
"PM10": {"path-name": "risk-level", "domain-min": 0.0, "domain-max": 100.0, "brightness": 254, "transition-time": 9}}
"""

from scs_core.data.json import JSONify

# from scs_host.sys.host import Host

from scs_philips_hue.config.chroma_conf import ChromaConfSet


# --------------------------------------------------------------------------------------------------------------------

chromas = ChromaConfSet({})
chromas.add('TEST', 'risk-level', 5, 30, 254, 9)
print(chromas)
print("-")


print("JSON...")
print(JSONify.dumps(chromas))
print("-")

# print("save...")
# chromas.save(Host)
# print("-")
#
# chromas = ChromaConfSet.load(Host)
#
# print("load...")
# print(chromas)
# print("-")
