#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"topic-path": "/orgs/south-coast-science-demo/brighton/loc/1/particulates", "document-node": "val.pm10"}
"""

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_philips_hue.config.domain_conf import DomainConf


# --------------------------------------------------------------------------------------------------------------------

topic_path = '/orgs/south-coast-science-demo/brighton/loc/1/particulates'
document_node = 'val.pm10'

conf = DomainConf(topic_path, document_node)

print("build...")
print(conf)
print("-")

print("JSON...")
print(JSONify.dumps(conf))
print("-")

print("save...")
conf.save(Host)
print("-")

conf = DomainConf.load(Host)

print("load...")
print(conf)
print("-")
