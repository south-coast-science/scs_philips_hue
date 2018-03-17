#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The desk_conf utility is used to specify which lamps should be driven by the desk utility.

EXAMPLES
./desk_conf.py -a scs-hcl-001

FILES
~/SCS/hue/desk_conf.json

DOCUMENT EXAMPLE
{"lamp-names": ["scs-hcl-001", "scs-hcl-002"]}

SEE ALSO
scs_philips_hue/desk.py
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
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # DeskConf...
    conf = DeskConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.add_lamp:
        if conf is None:
            conf = DeskConf([])

        conf.add_lamp(cmd.add_lamp)
        conf.save(Host)

    if cmd.remove_lamp:
        if conf is None:
            conf = DeskConf([])

        conf.remove_lamp(cmd.remove_lamp)
        conf.save(Host)

    if cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
