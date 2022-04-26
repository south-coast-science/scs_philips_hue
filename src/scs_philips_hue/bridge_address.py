#!/usr/bin/env python3

"""
Created on 2 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_analysis

DESCRIPTION
The bridge_address utility is used to

SYNOPSIS
bridge_address.py [{ [-e ENDPOINT] [-a API_KEY] | -d }] [-v]

EXAMPLES
bridge_address.py -e aws.southcoastscience.com -a de92c5ff-b47a-4cc4-a04c-62d684d64a1f

FILES
~/SCS/aws/bridge_address.json

DOCUMENT EXAMPLE
{"endpoint": "aws.southcoastscience.com", "api-key": "de92c5ff-b47a-4cc4-a04c-62d684d64a1f"}

SEE ALSO
"""

import sys

from scs_core.data.json import JSONify

from scs_core.sys.ipv4_address import IPv4Address
from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_bridge_address import CmdBridgeAddress
from scs_philips_hue.config.bridge_address import BridgeAddress


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdBridgeAddress()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    Logging.config('bridge_address', verbose=cmd.verbose)
    logger = Logging.getLogger()

    if cmd.set_dot_decimal is not None and not IPv4Address.is_valid(cmd.set_dot_decimal):
        logger.error("the IPv4 address '%s' is not valid." % cmd.set_dot_decimal)
        exit(2)

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # APIAuth...
    address = BridgeAddress.load(Host, skeleton=True)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set_dot_decimal:
        address = BridgeAddress(IPv4Address.construct(cmd.set_dot_decimal))
        address.save(Host)

    if cmd.delete:
        address.delete(Host)
        address = None

    if address is not None and address.ipv4 is not None:
        print(JSONify.dumps(address))
