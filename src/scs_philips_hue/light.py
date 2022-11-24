#!/usr/bin/env python3

"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

DESCRIPTION
The light utility is used to shifter a Philips Hue light bulb with a Philips Hue bridge device, to update bulb
settings.

If a bridge address has been stored, this is used to find the bridge. Otherwise a UPnP or IP scan is attempted.

SYNOPSIS
light.py { -a SERIAL_NUMBER | -s | -l | -d INDEX | -n INDEX NAME } [-v]

EXAMPLES
./light.py -v -a AA8A5F

FILES
~/SCS/hue/bridge_credentials.json

DOCUMENT EXAMPLE - OUTPUT
{"5": {"state": {"on": false, "bri": 0, "hue": 0, "sat": 0, "effect": "none", "transitiontime": null, "xy": [0.0, 0.0],
"ct": 0, "alert": "none", "colormode": "hs", "reachable": false}, "swupdate": {"state": "transferring",
"lastinstall": null}, "type": "Extended color light", "name": "scs-hcl-001", "modelid": "LCT015",
"manufacturername": "Philips", "uniqueid": "00:17:88:01:03:54:25:66-0b", "swversion": "1.19.0_r19755",
"swconfigid": "A724919D", "productid": "Philips-LCT015-1-A19ECLv5"}}


SEE ALSO
scs_philips_hue/bridge
scs_philips_hue/join

BUGS
The light search function is not always successful if lights have been previously registered on the bridge. If a search
does not find the light, then the light should be acquired with -a SERIAL_NUMBER.
"""

import sys
import time

from scs_core.client.network import Network
from scs_core.client.resource_unavailable_exception import ResourceUnavailableException

from scs_core.data.json import JSONify

from scs_core.sys.http_exception import HTTPException
from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_light import CmdLight

from scs_philips_hue.config.bridge_address import BridgeAddress
from scs_philips_hue.config.bridge_credentials import BridgeCredentials

from scs_philips_hue.discovery.discovery import Discovery

from scs_philips_hue.data.light.light_device import LightDevice

from scs_philips_hue.manager.light_manager import LightManager


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    address = None
    bridge = None
    manager = None
    response = None

    initial_state = {}

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdLight()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    Logging.config('light', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # check...

        if not Network.is_available():
            logger.info("waiting for network")
            Network.wait()


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # credentials...
        credentials = BridgeCredentials.load(Host)

        if credentials.bridge_id is None:
            logger.error("BridgeCredentials not available.")
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

            logger.info(bridge)
            ip_address = bridge.ip_address

        # manager...
        manager = LightManager(ip_address, credentials.username)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # add...
        if cmd.add:
            device = LightDevice(cmd.add)
            response = manager.search(device)

            while True:
                time.sleep(2.0)
                scan = manager.find_new()

                if not scan.is_active():
                    break

            for entry in scan.entries:
                print(JSONify.dumps(entry, indent=cmd.indent))

        # search...
        if cmd.search:
            response = manager.search()

            while True:
                time.sleep(2.0)
                scan = manager.find_new()

                if not scan.is_active():
                    break

            for entry in scan.entries:
                print(JSONify.dumps(entry, indent=cmd.indent))

        # delete...
        if cmd.delete:
            response = manager.delete(cmd.delete)

        # name...
        if cmd.name:
            response = manager.rename(cmd.name[0], cmd.name[1])

        if response:
            logger.info(response)

        # result...
        if cmd.name or cmd.delete or cmd.list:
            lights = manager.find_all()

            for light in lights:
                print(JSONify.dumps(light, indent=cmd.indent))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except (ConnectionError, HTTPException) as ex:
        logger.error(repr(ex))

    except ResourceUnavailableException as ex:
        logger.error(repr(ex))

    except KeyboardInterrupt:
        print(file=sys.stderr)

    except TimeoutError:
        logger.error("Timeout")
