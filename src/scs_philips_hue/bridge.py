#!/usr/bin/env python3

"""
Created on 11 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

DESCRIPTION
The bridge utility is used to interrogate and update the Philips Hue Bridge device.

If a bridge address has been stored, this is used to find the bridge. Otherwise a UPnP or IP scan is attempted.

SYNOPSIS
bridge.py [-n NAME] [-p PORTAL_SERVICES] [-c CHECK_UPDATE] [-u DO_UPDATE] [-z CHANNEL] [-v]

EXAMPLES
./bridge.py -n scs-phb-001 -v

FILES
~/SCS/hue/bridge_credentials.json

DOCUMENT EXAMPLE
{"bridge-id": "001788fffe795620", "username": "TIYoqrnwkvyODu8xE9zvRxjIJSRSde0qUzUqqIr7"}

SEE ALSO
scs_philips_hue/bridge_address
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
from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_bridge import CmdBridge

from scs_philips_hue.config.bridge_address import BridgeAddress
from scs_philips_hue.config.bridge_credentials import BridgeCredentials

from scs_philips_hue.data.bridge.bridge_config import BridgeConfig
from scs_philips_hue.data.bridge.sw_update import SWUpdate

from scs_philips_hue.discovery.discovery import Discovery

from scs_philips_hue.manager.bridge_manager import BridgeManager


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    address = None
    bridge = None
    response = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdBridge()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    Logging.config('bridge', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # check...

        if not Network.is_available():
            logger.info("waiting for network.")
            Network.wait()


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # credentials...
        credentials = BridgeCredentials.load(Host)

        if credentials.bridge_id is None:
            logger.error("no stored credentials")
            exit(1)

        logger.info(credentials)

        # address...
        address = BridgeAddress.load(Host)

        if address:
            logger.info(address)
            ip_address = address.ipv4.dot_decimal()

        else:
            # bridge...
            logger.info("looking for bridge...")

            discovery = Discovery(Host)
            bridge = discovery.find(credentials)

            if bridge is None:
                logger.error("no bridge matching the stored credentials.")
                exit(1)

            if bridge.ip_address is None:
                logger.error("bridge has no IP address.")
                exit(1)

            logger.info(bridge)
            ip_address = bridge.ip_address

        # manager...
        manager = BridgeManager(ip_address, credentials.username)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # initial state...
        config = manager.find()

        # name...
        if cmd.name:
            config = BridgeConfig(name=cmd.name)
            response = manager.set_config(config)

        # portal services...
        if cmd.portal_services:
            config = BridgeConfig(portal_services=cmd.portal_services)
            response = manager.set_config(config)

        # check for update...
        if cmd.check_update:
            config = BridgeConfig(sw_update=SWUpdate(check_for_update=cmd.check_update))
            response = manager.set_config(config)

        # do update...
        if cmd.do_update:
            if config.sw_update.update_state != SWUpdate.UPDATE_AVAILABLE:
                logger.error("no software update available.")
                exit(1)

            config = BridgeConfig(sw_update=SWUpdate(update_state=SWUpdate.UPDATE_PERFORM))
            response = manager.set_config(config)

        # zigbee...
        if cmd.zigbee_channel:
            config = BridgeConfig(zigbee_channel=cmd.zigbee_channel)
            response = manager.set_config(config)

        if response:
            logger.info(response)

        config = manager.find()
        print(JSONify.dumps(config, indent=cmd.indent))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except (ConnectionError, HTTPException) as ex:
        logger.error("%s: %s" % (ex.__class__.__name__, ex))

    except ResourceUnavailableException as ex:
        logger.error(repr(ex))

    except KeyboardInterrupt:
        print(file=sys.stderr)

    except TimeoutError:
        logger.error("Timeout")
