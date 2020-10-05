#!/usr/bin/env python3

"""
Created on 4 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"name": "test", "points": [[0.74, 0.26], [0.48, 0.41], [0.08, 0.84]]}
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
print("-")

print("defaults...")
defaults = ChromaPath.defaults()
for default in defaults:
    print(default)
print("-")

print("risk...")
risk = ChromaPath.load_default('risk')
print(risk)
print("-")
