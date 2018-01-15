#!/usr/bin/env python3

"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./light.py -v -a AA8A5F
"""

import sys
import time

from scs_core.data.json import JSONify

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_light import CmdLight

from scs_philips_hue.config.credentials import Credentials

from scs_philips_hue.data.light.light_device import LightDevice

from scs_philips_hue.manager.light_manager import LightManager
from scs_philips_hue.manager.upnp_discovery import UPnPDiscovery


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdLight()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)

    initial_state = {}
    manager = None

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
        manager = LightManager(HTTPClient(), bridge.ip_address, credentials.username)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # add...
        if cmd.add:
            device = LightDevice(cmd.add)
            response = manager.search(device)

            if cmd.verbose:
                print(response, file=sys.stderr)

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
                print(response, file=sys.stderr)

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
                print(response, file=sys.stderr)

        # name...
        if cmd.name:
            response = manager.rename(cmd.name[0], cmd.name[1])

            if cmd.verbose:
                print(response, file=sys.stderr)

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