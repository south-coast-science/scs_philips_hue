#!/usr/bin/env python3

"""
Created on 3 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The join utility is used to register a controller device - the device hosting this software - with a Philips Hue Bridge.
Before running join, the big button on the top of the Philips Hue Bridge must be pressed!

The bridge_credentials.json document created by the join utility is used by the bridge, desk, light, and user utilities.

SYNOPSIS
join.py [-v]

EXAMPLES
./join.py -v

FILES
~/SCS/hue/bridge_credentials.json

DOCUMENT EXAMPLE
{"bridge-id": "001788fffe795620", "username": "b8bvymOH-ceugK8gBOpjeNeL0OMhXOEBQZosfsTx"}

SEE ALSO
scs_philips_hue/bridge
scs_philips_hue/desk
scs_philips_hue/light
scs_philips_hue/user
"""

import sys

from scs_core.data.json import JSONify

from scs_host.client.http_client import HTTPClient
from scs_host.comms.stdio import StdIO
from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_simple import CmdSimple

from scs_philips_hue.config.bridge_credentials import BridgeCredentials

from scs_philips_hue.manager.bridge_manager import BridgeManager
from scs_philips_hue.manager.upnp_discovery import UPnPDiscovery
from scs_philips_hue.manager.user_manager import UserManager

from scs_philips_hue.data.client.client_description import ClientDescription
from scs_philips_hue.data.client.device_description import DeviceDescription


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSimple()

    if cmd.verbose:
        print("join: %s" % cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resource...

    # bridge...
    upnp = UPnPDiscovery(HTTPClient())

    bridges = upnp.find_all()

    if len(bridges) == 0:
        print("join: no bridge found", file=sys.stderr)
        bridge = None
        exit(0)

    elif len(bridges) == 1:
        bridge = bridges.pop()

    else:
        for i in range(len(bridges)):
            print("%d: %s" % ((i + 1), bridges[i]))

        index = StdIO.prompt("Bridge (1 - %d) ?: " % len(bridges))
        bridge = bridges[int(index) - 1]

    if cmd.verbose:
        print("join: %s" % bridge, file=sys.stderr)

    # manager...
    bridge_manager = BridgeManager(HTTPClient(), bridge.ip_address, None)

    # device...
    client = ClientDescription(ClientDescription.APP, Host.name())
    device = DeviceDescription(client)

    if cmd.verbose:
        print("join: %s" % device, file=sys.stderr)

    sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    # join...
    response = None

    try:
        response = bridge_manager.register(device)
    except TimeoutError:
        print("join: bridge not found", file=sys.stderr)
        exit(1)

    if response.has_errors():
        for error in response.errors:
            print("join: error: %s" % error.description, file=sys.stderr)
        exit(1)

    # save credentials...
    success = response.successes.pop()

    credentials = BridgeCredentials(bridge.id, success.value)
    credentials.save(Host)

    # delete old whitelist entries for this user...
    user_manager = UserManager(HTTPClient(), bridge.ip_address, credentials.username)

    users = user_manager.find_all()

    for user in users:
        if user.description.user == Host.name() and user.username != credentials.username:
            response = user_manager.delete(user.username)

    # report...
    bridge_manager = BridgeManager(HTTPClient(), bridge.ip_address, credentials.username)
    config = bridge_manager.find()

    print(JSONify.dumps(credentials))
