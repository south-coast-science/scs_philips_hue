#!/usr/bin/env python3

"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./light.py
"""

import json
import sys
import time

from collections import OrderedDict

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_light import CmdLight

from scs_philips_hue.config.credentials import Credentials

from scs_philips_hue.data.light.light_state import LightState

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

        # search...
        if cmd.search:
            response = manager.search()

            if cmd.verbose:
                print("scanning...", file=sys.stderr)

            while True:
                time.sleep(2.0)
                scan = manager.find_new()

                if not scan.is_active():
                    break

            for entry in scan.entries:
                print(JSONify.dumps(entry))

        # list...
        elif cmd.list:
            response = manager.find_all()
            for item in response:
                print(JSONify.dumps(item))

        # name...
        elif cmd.name:
            response = manager.rename(cmd.name[0], cmd.name[1])
            print(JSONify.dumps(response))

        # delete...
        elif cmd.delete:
            response = manager.delete(cmd.delete)
            print(JSONify.dumps(response))

        # run...
        elif cmd.run:
            # save initial states...
            for index in cmd.run_indices:
                initial_state[index] = manager.find(index).state

            # read stdin...
            for line in sys.stdin:
                datum = line.strip()

                if datum is None:
                    break

                if cmd.echo:
                    print(datum)
                    sys.stdout.flush()

                try:
                    jdict = json.loads(datum, object_pairs_hook=OrderedDict)
                except ValueError:
                    continue

                state = LightState.construct_from_jdict(jdict)

                for index in cmd.run_indices:
                    response = manager.set_state(index, state)

                    if cmd.verbose:
                        print(response, file=sys.stderr)
                        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("light: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        if cmd.run and manager:
            for index, state in initial_state.items():
                state = LightState(on=state.on, bri=state.bri, hue=state.hue, sat=state.sat, transition_time=1.0)
                manager.set_state(index, state)
