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

from scs_philips_hue.config.chroma_conf import ChromaConf


# --------------------------------------------------------------------------------------------------------------------

conf = ChromaConf('risk-level', 5, 30, 254, 9)
print(conf)
print("-")


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
