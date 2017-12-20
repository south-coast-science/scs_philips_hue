#!/usr/bin/env python3

"""
Created on 25 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./osio_mqtt_subscriber.py /orgs/south-coast-science-demo/brighton/loc/1/particulates | \
    ./node.py /orgs/south-coast-science-demo/brighton/loc/1/particulates.val.pm2p5 | \
    ./chroma.py -d 0 50 -r G R -t 9.0 -b 128 -v | \
    ./desk.py -v -e -r scs-hcl-001
"""

import json
import sys
import time

from collections import OrderedDict

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_desk import CmdDesk

from scs_philips_hue.config.credentials import Credentials

from scs_philips_hue.data.light.light_state import LightState

from scs_philips_hue.manager.light_manager import LightManager
from scs_philips_hue.manager.upnp_discovery import UPnPDiscovery


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdDesk()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)

    manager = None
    timeout = False

    indices = {}
    initial_state = {}

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

        # check for bridge availability...
        timeout = time.time() + 10

        while True:
            try:
                manager.find_all()
                break

            except OSError:
                if time.time() > timeout:
                    print("bridge could not be found", file=sys.stderr)
                    exit(1)

                time.sleep(1)
                continue

        # indices...
        for name in cmd.args:
            indices[name] = manager.find_indices_for_name(name)

            if len(indices[name]) == 0:
                print("warning: no light found for name: %s" % name, file=sys.stderr)

            # save initial states...
            for index in indices[name]:
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

            for name in cmd.args:
                for index in indices[name]:
                    response = manager.set_state(index, state)

                    if cmd.verbose:
                        print(response, file=sys.stderr)
                        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("desk: KeyboardInterrupt", file=sys.stderr)

    except TimeoutError:
        print("desk: Timeout", file=sys.stderr)

    finally:
        if manager and not timeout:
            for index, state in initial_state.items():
                state = LightState(on=state.on, bri=state.bri, hue=state.hue, sat=state.sat, transition_time=1.0)
                manager.set_state(index, state)
