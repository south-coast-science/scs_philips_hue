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

from scs_philips_hue.config.chroma_path import ChromaPath


# --------------------------------------------------------------------------------------------------------------------

name = 'test'
print(name)

points = [ChromaPath.CANONICAL_CHROMAS['R'], ChromaPath.CANONICAL_CHROMAS['G']]
print(points)

path = ChromaPath(name, points)
print(path)
print("-")

print("insert...")
path.insert_point(1, ChromaPath.CANONICAL_CHROMAS['W'])
print(path)
print("-")

print("persist...")
path.save(Host)
path = path.load(Host, name)
print(path)
print("-")

print("remove...")
path.remove_point(1)
print(path)
print("-")

print(JSONify.dumps(path.as_json()))
