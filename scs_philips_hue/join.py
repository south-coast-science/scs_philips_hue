#!/usr/bin/env python3

"""
Created on 3 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./join.py -v
"""

import sys

from scs_core.data.json import JSONify

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_simple import CmdSimple

from scs_philips_hue.config.credentials import Credentials

from scs_philips_hue.manager.bridge_manager import BridgeManager
from scs_philips_hue.manager.upnp_discovery import UPnPDiscovery

from scs_philips_hue.data.client.client_description import ClientDescription
from scs_philips_hue.data.client.device_description import DeviceDescription


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSimple()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resource...

    # bridge...
    upnp = UPnPDiscovery(HTTPClient())

    bridges = upnp.find_all()
    bridge = bridges.pop()                  # TODO: handle the case of multiple bridges

    if cmd.verbose:
        print(bridge, file=sys.stderr)

    # manager...
    manager = BridgeManager(HTTPClient(), bridge.ip_address, None)

    # device...
    client = ClientDescription(ClientDescription.APP, Host.name())
    device = DeviceDescription(client)

    if cmd.verbose:
        print(device, file=sys.stderr)

    sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    # join...
    response = None

    try:
        response = manager.register(device)
    except TimeoutError:
        print("bridge not found", file=sys.stderr)
        exit(1)

    if response.has_errors():
        for error in response.errors:
            print("error: %s" % error.description, file=sys.stderr)
        exit(1)

    # save credentials...
    success = response.successes.pop()

    credentials = Credentials(bridge.id, success.value)
    credentials.save(Host)

    # report...
    manager = BridgeManager(HTTPClient(), bridge.ip_address, credentials.username)
    config = manager.find()

    print(JSONify.dumps(credentials))
