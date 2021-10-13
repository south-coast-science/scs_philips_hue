#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

DESCRIPTION
The desk_conf utility is used to specify which lamps should be driven by the desk utility.

SYNOPSIS
desk_conf.py [-n NAME] [{ -a LAMP_NAME | -r LAMP_NAME | -d }] [-v]

EXAMPLES
./desk_conf.py -a scs-hcl-001

FILES
~/SCS/hue/desk_conf.json

DOCUMENT EXAMPLE
{"lamp-names": ["scs-hcl-001", "scs-hcl-002"]}

SEE ALSO
scs_philips_hue/desk
"""

import sys

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_desk_conf import CmdDeskConf
from scs_philips_hue.config.desk_conf import DeskConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdDeskConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("desk_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # DeskConf...
    conf = DeskConf.load(Host, name=cmd.name)

    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.add_lamp:
        if conf is None:
            conf = DeskConf([], name=cmd.name)

        conf.add_lamp(cmd.add_lamp)
        conf.save(Host)

    if cmd.remove_lamp:
        if conf is None:
            conf = DeskConf([], name=cmd.name)

        conf.remove_lamp(cmd.remove_lamp)
        conf.save(Host)

    if cmd.delete:
        conf.delete(Host, name=cmd.name)
        conf = None

    if conf:
        print(JSONify.dumps(conf, indent=cmd.indent))
