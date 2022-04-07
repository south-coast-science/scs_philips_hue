#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

DESCRIPTION
The desk_conf utility is used to specify which lamps should be driven by the desk utility.

SYNOPSIS
Usage: desk_conf.py [-n NAME { -a LAMP_NAME | -r LAMP_NAME | -d }] [-i INDENT] [-v]

EXAMPLES
./desk_conf.py -a scs-hcl-001

FILES
~/SCS/hue/desk_conf.json

DOCUMENT EXAMPLE
{"NO2": {"lamp-names": {"lamp-names": ["1600-1"]}}}

SEE ALSO
scs_philips_hue/desk
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_desk_conf import CmdDeskConf
from scs_philips_hue.config.desk_conf import DeskConf, DeskConfSet


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    desk = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdDeskConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    Logging.config('desk_conf', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # DeskConf...
    desks = DeskConfSet.load(Host, skeleton=True)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        desk = desks.conf(cmd.name)

    if cmd.add_lamp:
        if desk is None:
            desk = DeskConf([])

        desk.add_lamp(cmd.add_lamp)

        desks.add(cmd.name, desk)
        desks.save(Host)

    if cmd.remove_lamp:
        if desk is not None:
            desk.remove_lamp(cmd.remove_lamp)

            if len(desk) == 0:
                desks.remove(cmd.name)

            desks.save(Host)

    if cmd.delete:
        desks.remove(cmd.name)
        desks.save(Host)

    if desks:
        print(JSONify.dumps(desks, indent=cmd.indent))
