#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

DESCRIPTION
The domain_conf utility is used to specify an environmental data messaging topic path, plus a leaf node within
documents delivered on that messaging topic. Together, these two parameters yield a scalar value that can be
accepted by a mapping utility such as chroma.

The domain_conf.json document managed by the domain_conf utility is used by the aws_mqtt_subscriber,
osio_mqtt_subscriber, and node utilities.

SYNOPSIS
domain_conf.py [{ [-t TOPIC_PATH] [-n DOCUMENT_NODE] | -x }] [-v]

EXAMPLES
./domain_conf.py -t /orgs/south-coast-science-demo/brighton/loc/1/particulates -n val.pm10

FILES
~/SCS/hue/domain_conf.json

DOCUMENT EXAMPLE
{"topic-path": "/orgs/south-coast-science-demo/brighton/loc/1/particulates", "document-node": "val.pm10"}

SEE ALSO
scs_philips_hue/aws_mqtt_subscriber
scs_philips_hue/osio_mqtt_subscriber
scs_philips_hue/node
"""

import sys

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_domain_conf import CmdDomainConf
from scs_philips_hue.config.domain_conf import DomainConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdDomainConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("domain_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # ChromaConf...
    conf = DomainConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("domain_conf: no configuration is stored - you must therefore set all fields.", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(2)

        topic_path = conf.topic_path if cmd.topic_path is None else cmd.topic_path
        document_node = conf.document_node if cmd.document_node is None else cmd.document_node

        conf = DomainConf(topic_path, document_node)
        conf.save(Host)

    if cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf, indent=cmd.indent))
