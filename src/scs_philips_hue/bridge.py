#!/usr/bin/env python3

"""
Created on 11 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

DESCRIPTION
The bridge utility is used to interrogate and update the Philips Hue Bridge device.

SYNOPSIS
bridge.py [-n NAME] [-p PORTAL_SERVICES] [-c CHECK_UPDATE] [-u DO_UPDATE] [-z CHANNEL] [-v]

EXAMPLES
./bridge.py -n scs-phb-001 -v

FILES
~/SCS/hue/bridge_credentials.json

DOCUMENT EXAMPLE
{"bridge-id": "001788fffe795620", "username": "TIYoqrnwkvyODu8xE9zvRxjIJSRSde0qUzUqqIr7"}

SEE ALSO
scs_philips_hue/join
scs_philips_hue/user

RESOURCES
https://developers.meethue.com/content/configuring-hue-without-phone-app-unable-update-software
"""

import sys

from scs_core.client.network import Network
from scs_core.client.resource_unavailable_exception import ResourceUnavailableException

from scs_core.data.json import JSONify
from scs_core.sys.http_exception import HTTPException

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_bridge import CmdBridge

from scs_philips_hue.config.bridge_credentials import BridgeCredentials

from scs_philips_hue.data.bridge.bridge_config import BridgeConfig
from scs_philips_hue.data.bridge.sw_update import SWUpdate

from scs_philips_hue.discovery.discovery import Discovery

from scs_philips_hue.manager.bridge_manager import BridgeManager


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    bridge = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdBridge()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("bridge: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    try:
        # ------------------------------------------------------------------------------------------------------------
        # check...

        if not Network.is_available():
            if cmd.verbose:
                print("bridge: waiting for network.", file=sys.stderr)
                sys.stderr.flush()

            Network.wait()


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # credentials...
        credentials = BridgeCredentials.load(Host)

        if credentials.bridge_id is None:
            print("bridge: no stored credentials")
            exit(1)

        if cmd.verbose:
            print("bridge: %s" % credentials, file=sys.stderr)

        # bridge...
        if cmd.verbose:
            print("bridge: looking for bridge...", file=sys.stderr)

        discovery = Discovery(Host)
        bridge = discovery.find(credentials)

        if bridge is None:
            print("bridge: no bridge matching the stored credentials")
            exit(1)

        if cmd.verbose:
            print("bridge: %s" % bridge, file=sys.stderr)

        sys.stderr.flush()

        # manager...
        manager = BridgeManager(bridge.ip_address, credentials.username)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # initial state...
        config = manager.find()

        # name...
        if cmd.name:
            config = BridgeConfig(name=cmd.name)
            response = manager.set_config(config)

            if cmd.verbose:
                print("bridge: %s" % response, file=sys.stderr)

        # portal services...
        if cmd.portal_services:
            config = BridgeConfig(portal_services=cmd.portal_services)
            response = manager.set_config(config)

            if cmd.verbose:
                print("bridge: %s" % response, file=sys.stderr)

        # check for update...
        if cmd.check_update:
            config = BridgeConfig(sw_update=SWUpdate(check_for_update=cmd.check_update))
            response = manager.set_config(config)

            if cmd.verbose:
                print("bridge: %s" % response, file=sys.stderr)

        # do update...
        if cmd.do_update:
            if config.sw_update.update_state != SWUpdate.UPDATE_AVAILABLE:
                print("bridge: no software update available")
                exit(1)

            config = BridgeConfig(sw_update=SWUpdate(update_state=SWUpdate.UPDATE_PERFORM))
            response = manager.set_config(config)

            if cmd.verbose:
                print("bridge: %s" % response, file=sys.stderr)

        # zigbee...
        if cmd.zigbee_channel:
            config = BridgeConfig(zigbee_channel=cmd.zigbee_channel)
            response = manager.set_config(config)

            if cmd.verbose:
                print("bridge: %s" % response, file=sys.stderr)

        config = manager.find()
        print(JSONify.dumps(config, indent=cmd.indent))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except (ConnectionError, HTTPException) as ex:
        print("bridge: %s: %s" % (ex.__class__.__name__, ex), file=sys.stderr)

    except ResourceUnavailableException as ex:
        print("bridge: %s" % repr(ex), file=sys.stderr)

    except KeyboardInterrupt:
        if cmd.verbose:
            print("bridge: KeyboardInterrupt", file=sys.stderr)

    except TimeoutError:
        print("bridge: Timeout", file=sys.stderr)
