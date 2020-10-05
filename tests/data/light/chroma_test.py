#!/usr/bin/env python3

"""
Created on 5 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_philips_hue.config.chroma_conf import ChromaConf


# --------------------------------------------------------------------------------------------------------------------

conf = ChromaConf('risk', 5, 30, 254, 9)
print(conf)
print("-")

path = conf.path()
print(path)
print("len: %s" % len(path))
print("-")

mapping = conf.mapping(path)
print(mapping)
print("len: %s" % len(mapping))
print("-")

