#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"min": {"domain-min": 0, "range-min": [0.08, 0.84]},
"intervals": [{"domain-max": 50, "range-max": [0.48, 0.41]}, {"domain-max": 100, "range-max": [0.74, 0.26]}],
"brightness": 128, "transition-time": 9}
"""

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_philips_hue.config.chroma_conf import ChromaConf, ChromaMin, ChromaInterval


# --------------------------------------------------------------------------------------------------------------------

domain_min = 0
domain_mid = 50
domain_max = 100

range_min = ChromaConf.CANONICAL_CHROMAS['G']
range_mid = ChromaConf.CANONICAL_CHROMAS['W']
range_max = ChromaConf.CANONICAL_CHROMAS['R']

brightness = 128
transition_time = 9

minimum = ChromaMin(domain_min, range_min)

intervals = [ChromaInterval(domain_mid, range_mid), ChromaInterval(domain_max, range_max)]

conf = ChromaConf(minimum, intervals, brightness, transition_time)

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
