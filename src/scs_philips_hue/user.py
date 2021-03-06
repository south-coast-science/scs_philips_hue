#!/usr/bin/env python3

"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

DESCRIPTION
The user utility is used to manage user accounts or "whitelist entries" on a Philips Hue Bridge device.

Note that the user JSON document presented by the user utility has a description field of the form
app#user-name. When a delete command is performed, only the user-name component should be used to identify
the user.

SYNOPSIS
user.py {-d USER | -l }  [-v]

EXAMPLES
./user.py -d bruno.local

FILES
~/SCS/hue/bridge_credentials.json

DOCUMENT EXAMPLE - OUTPUT
{"last use date": "2017-11-26T10:29:17", "create date": "2017-11-26T10:08:13",
"description": "scs-hue-connector#scs-rpi-013"}

SEE ALSO
scs_philips_hue/join
scs_philips_hue/bridge
scs_philips_hue/desk
"""

import sys

from scs_core.data.json import JSONify

from scs_host.sys.host import Host
from scs_core.sys.http_exception import HTTPException

from scs_philips_hue.cmd.cmd_user import CmdUser

from scs_philips_hue.config.bridge_credentials import BridgeCredentials

from scs_philips_hue.discovery.discovery import Discovery

from scs_philips_hue.manager.user_manager import UserManager


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    application_key = ''

    bridge = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdUser()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("user: %s" % cmd, file=sys.stderr)

    try:

        # -------------------------------------------------------------------------------------------------------------
        # resource...

        # credentials...
        credentials = BridgeCredentials.load(Host)

        if credentials.bridge_id is None:
            print("user: no stored credentials", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("user: %s" % credentials, file=sys.stderr)

        # bridge...
        if cmd.verbose:
            print("user: looking for bridge...", file=sys.stderr)

        discovery = Discovery(Host)
        bridge = discovery.find(credentials)

        if bridge is None:
            print("user: no bridge matching the stored credentials", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("user: %s" % bridge, file=sys.stderr)

        sys.stderr.flush()

        # manager...
        manager = UserManager(bridge.ip_address, credentials.username)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        users = manager.find_all()

        if cmd.delete:
            for user in users:
                if user.description.user == cmd.delete:
                    response = manager.delete(application_key, user.username)

                    if cmd.verbose:
                        print("user: %s" % response, file=sys.stderr)
                        sys.stderr.flush()

        else:
            for user in users:
                print(JSONify.dumps(user))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except (ConnectionError, HTTPException) as ex:
        print("user: %s: %s" % (ex.__class__.__name__, ex), file=sys.stderr)

    except KeyboardInterrupt:
        if cmd.verbose:
            print("user: KeyboardInterrupt", file=sys.stderr)
