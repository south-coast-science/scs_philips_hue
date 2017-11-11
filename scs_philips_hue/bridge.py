#!/usr/bin/env python3

"""
Created on 11 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./bridge.py
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_simple import CmdSimple

from scs_philips_hue.config.credentials import Credentials

from scs_philips_hue.manager.bridge_manager import BridgeManager
from scs_philips_hue.manager.upnp_discovery import UPnPDiscovery


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSimple()

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

        config = manager.find_config()
        print(JSONify.dumps(config))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("bridge: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)
