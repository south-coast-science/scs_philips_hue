#!/usr/bin/env python3

"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./user.py -v
"""

import sys

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_simple import CmdSimple

from scs_philips_hue.config.credentials import Credentials

from scs_philips_hue.manager.upnp_discovery import UPnPDiscovery
from scs_philips_hue.manager.user_manager import UserManager


# TODO: required functions: list, remove user

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSimple()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resource...

    # credentials...
    credentials = Credentials.load(Host)

    if credentials.bridge_id is None:
        print("no stored credentials")
        exit(1)

    if cmd.verbose:
        print(credentials, file=sys.stderr)

    # bridge...
    upnp = UPnPDiscovery(HTTPClient())
    bridge = upnp.find(credentials.bridge_id)

    if bridge is None:
        print("no bridge matching the stored credentials")
        exit(1)

    if cmd.verbose:
        print(bridge, file=sys.stderr)

    sys.stderr.flush()

    # manager...
    manager = UserManager(HTTPClient(), bridge.ip_address, credentials.username)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    users = manager.find_all()

    for user in users:
        print(user)
