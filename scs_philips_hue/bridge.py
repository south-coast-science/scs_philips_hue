#!/usr/bin/env python3

"""
Created on 11 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./bridge.py -n scs-phb-001 -v
"""

import sys

from scs_core.data.json import JSONify

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_bridge import CmdBridge

from scs_philips_hue.config.credentials import Credentials

from scs_philips_hue.data.bridge.bridge_config import BridgeConfig
from scs_philips_hue.data.bridge.sw_update import SWUpdate

from scs_philips_hue.manager.bridge_manager import BridgeManager
from scs_philips_hue.manager.upnp_discovery import UPnPDiscovery


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdBridge()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

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
        manager = BridgeManager(HTTPClient(), bridge.ip_address, credentials.username)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # name...
        if cmd.name:
            config = BridgeConfig(name=cmd.name)
            response = manager.set_config(config)

            if cmd.verbose:
                print(response, file=sys.stderr)

        # update...
        if cmd.update:
            config = BridgeConfig(sw_update=SWUpdate(check_for_update=True))
            response = manager.set_config(config)

            if cmd.verbose:
                print(response, file=sys.stderr)

        # zigbee...
        if cmd.zigbee:
            config = BridgeConfig(zigbee_channel=cmd.zigbee)
            response = manager.set_config(config)

            if cmd.verbose:
                print(response, file=sys.stderr)

        config = manager.find()
        print(JSONify.dumps(config))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("bridge: KeyboardInterrupt", file=sys.stderr)

    except TimeoutError:
        print("bridge: Timeout", file=sys.stderr)
