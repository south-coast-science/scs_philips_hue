#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Creates or deletes ChromaConf document.

document example:
{"topic-path": "/orgs/south-coast-science-demo/brighton/loc/1/particulates", "document-node": "val.pm10"}

command line example:
./domain_conf.py -t /orgs/south-coast-science-demo/brighton/loc/1/particulates -n val.pm10
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
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # ChromaConf...
    conf = DomainConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("No configuration is stored. domain_conf must therefore set all fields:", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(1)

        topic_path = conf.topic_path if cmd.topic_path is None else cmd.topic_path
        document_node = conf.document_node if cmd.document_node is None else cmd.document_node

        conf = DomainConf(topic_path, document_node)
        conf.save(Host)

    if cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
