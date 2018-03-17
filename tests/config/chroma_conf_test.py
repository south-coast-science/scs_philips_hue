#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"domain-min": 0.0, "domain-max": 50.0, "range-min": [0.08, 0.84], "range-max": [0.74, 0.26],
"brightness": 128, "transition-time": 9}
"""

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_philips_hue.config.chroma_conf import ChromaConf


# --------------------------------------------------------------------------------------------------------------------

domain_min = 0.0
domain_max = 50.0

range_min = ChromaConf.CANONICAL_CHROMAS['G']
range_max = ChromaConf.CANONICAL_CHROMAS['R']

brightness = 128
transition_time = 9

conf = ChromaConf(domain_min, domain_max, range_min, range_max, brightness, transition_time)

print("build...")
print(conf)
print("-")

print("JSON...")
print(JSONify.dumps(conf))
print("-")

print("save...")
conf.save(Host)
print("-")

conf = ChromaConf.load(Host)

print("load...")
print(conf)
print("-")
