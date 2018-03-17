#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"lamp-names": ["scs-hcl-001", "scs-hcl-002"]}
"""

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_philips_hue.config.desk_conf import DeskConf


# --------------------------------------------------------------------------------------------------------------------

lamp_names = ['scs-hcl-001', 'scs-hcl-002']

conf = DeskConf(lamp_names)

print("build...")
print(conf)
print("-")

print("JSON...")
print(JSONify.dumps(conf))
print("-")

print("save...")
conf.save(Host)
print("-")

conf = DeskConf.load(Host)

print("load...")
print(conf)
print("-")
