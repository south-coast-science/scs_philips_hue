#!/usr/bin/env python3

"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./user.py -d bruno.local
"""

import sys

from scs_core.data.json import JSONify

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_user import CmdUser

from scs_philips_hue.config.bridge_credentials import BridgeCredentials

from scs_philips_hue.manager.upnp_discovery import UPnPDiscovery
from scs_philips_hue.manager.user_manager import UserManager


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdUser()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resource...

    # credentials...
    credentials = BridgeCredentials.load(Host)

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

    if cmd.delete:
        for user in users:
            if user.description.user == cmd.delete:
                response = manager.delete(user.username)

                if cmd.verbose:
                    print(response, file=sys.stderr)
                    sys.stderr.flush()

    else:
        for user in users:
            print(JSONify.dumps(user))
