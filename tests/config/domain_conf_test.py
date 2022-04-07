#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"topic-path": "/orgs/south-coast-science-demo/brighton/loc/1/particulates", "document-node": "val.pm10"}
"""

from scs_core.data.json import JSONify

# from scs_host.sys.host import Host

from scs_philips_hue.config.domain_conf import DomainConfSet


# --------------------------------------------------------------------------------------------------------------------

topic_path = '/orgs/south-coast-science-demo/brighton/loc/1/particulates'
document_node = 'val.pm10'

domains = DomainConfSet({})
domains.add('TEST', topic_path, document_node)

print("build...")
print(domains)
print("-")

print("JSON...")
print(JSONify.dumps(domains))
print("-")

# print("save...")
# conf.save(Host)
# print("-")
#
# domains = DomainConfSet.load(Host)
#
# print("load...")
# print(domains)
# print("-")
