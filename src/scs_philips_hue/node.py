#!/usr/bin/env python3

"""
Created on 11 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

May require DomainConf document.

command line example:
./osio_mqtt_subscriber.py -c | ./node.py -c
"""

import sys

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict

from scs_core.sys.exception_report import ExceptionReport

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_node import CmdNode
from scs_philips_hue.config.domain_conf import DomainConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNode()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # DomainConf...
        if cmd.use_domain_conf:
            domain = DomainConf.load(Host)
            topic_path = domain.topic_path + '.' + domain.document_node

            if domain is None:
                print("Domain not available.", file=sys.stderr)
                exit(1)

            if cmd.verbose:
                print(domain, file=sys.stderr)
        else:
            topic_path = cmd.topic_path


        # ------------------------------------------------------------------------------------------------------------
        # run...

        for line in sys.stdin:
            datum = PathDict.construct_from_jstr(line)

            if datum is None:
                continue

            if cmd.ignore and not datum.has_path(topic_path):
                continue

            node = datum.node(topic_path)

            print(JSONify.dumps(node))
            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("node: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)
