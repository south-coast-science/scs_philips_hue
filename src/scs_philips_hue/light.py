#!/usr/bin/env python3

"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

DESCRIPTION
The light utility is used to shifter a Philips Hue light bulb with a Philips Hue Bridge device, to update bulb
settings, or de-shifter the bulb.

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

from scs_core.data.json import JSONify

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_light import CmdLight

from scs_philips_hue.config.bridge_credentials import BridgeCredentials

from scs_philips_hue.discovery.discovery import Discovery

from scs_philips_hue.data.light.light_device import LightDevice

from scs_philips_hue.manager.light_manager import LightManager


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    bridge = None
    manager = None
    initial_state = {}

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdLight()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("light: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # credentials...
        credentials = BridgeCredentials.load(Host)

        if credentials.bridge_id is None:
            print("light: BridgeCredentials not available", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("light: %s" % credentials, file=sys.stderr)

        # bridge...
        discovery = Discovery(Host, HTTPClient())
        bridge = discovery.find(credentials)

        if cmd.verbose:
            print("light: looking for bridge...", file=sys.stderr)

        if bridge is None:
            print("light: no bridge matching the stored credentials", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("light: %s" % bridge, file=sys.stderr)

        sys.stderr.flush()

        # manager...
        manager = LightManager(HTTPClient(), bridge.ip_address, credentials.username)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # add...
        if cmd.add:
            device = LightDevice(cmd.add)
            response = manager.search(device)

            if cmd.verbose:
                print("light: %s" % response, file=sys.stderr)

            while True:
                time.sleep(2.0)
                scan = manager.find_new()

                if not scan.is_active():
                    break

            for entry in scan.entries:
                print(JSONify.dumps(entry))

        # search...
        if cmd.search:
            response = manager.search()

            if cmd.verbose:
                print("light: %s" % response, file=sys.stderr)

            while True:
                time.sleep(2.0)
                scan = manager.find_new()

                if not scan.is_active():
                    break

            for entry in scan.entries:
                print(JSONify.dumps(entry))

        # delete...
        if cmd.delete:
            response = manager.delete(cmd.delete)

            if cmd.verbose:
                print("light: %s" % response, file=sys.stderr)

        # name...
        if cmd.name:
            response = manager.rename(cmd.name[0], cmd.name[1])

            if cmd.verbose:
                print("light: %s" % response, file=sys.stderr)

        # result...
        if cmd.name or cmd.delete or cmd.list:
            lights = manager.find_all()

            for light in lights:
                print(JSONify.dumps(light))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("light: KeyboardInterrupt", file=sys.stderr)

    except TimeoutError:
        print("light: Timeout", file=sys.stderr)
