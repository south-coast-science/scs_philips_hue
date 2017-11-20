#!/usr/bin/env python3

"""
Created on 11 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./osio_mqtt_client.py /orgs/south-coast-science-demo/brighton/loc/1/particulates | \
    ./node.py /orgs/south-coast-science-demo/brighton/loc/1/particulates.val.pm2p5
"""

import sys

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict
from scs_core.sys.exception_report import ExceptionReport

from scs_philips_hue.cmd.cmd_node import CmdNode


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
        # run...

        for line in sys.stdin:
            datum = PathDict.construct_from_jstr(line)

            if datum is None:
                continue

            if cmd.ignore and not datum.has_path(cmd.path):
                continue

            node = datum.node(cmd.path)

            print(JSONify.dumps(node))
            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("node: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)
