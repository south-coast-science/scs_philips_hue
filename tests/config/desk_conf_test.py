#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"NO2": {"lamp-names": {"lamp-names": ["1600-1"]}}}
"""

from scs_core.data.json import JSONify

# from scs_host.sys.host import Host

from scs_philips_hue.config.desk_conf import DeskConfSet


# --------------------------------------------------------------------------------------------------------------------

lamp_names = ['scs-hcl-001', 'scs-hcl-002']

desks = DeskConfSet({})
desks.add('TEST', lamp_names)

print("build...")
print(desks)
print("-")

print("JSON...")
print(JSONify.dumps(desks))
print("-")

# print("save...")
# desks.save(Host)
# print("-")
#
# desks = DeskConfSet.load(Host)
#
# print("load...")
# print(desks)
# print("-")
