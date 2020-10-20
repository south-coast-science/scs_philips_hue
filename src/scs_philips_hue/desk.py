#!/usr/bin/env python3

"""
Created on 25 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

DESCRIPTION
The desk utility (a lighting control desk) is used to drive the Philips Hue Bridge device. Input data is received
from stdin, and is interpreted as a scs_philips_hue.data.light.LightState document.

In verbose mode, the desk utility provides a detailed report on the command outcome to stderr.

The desk utility requires the desk_conf.json document, specifying which light(s) should receive the LightState
command.

Note: this utility waits forever for a network connection and domain name server.

SYNOPSIS
desk.py [-n NAME] [-e] [-v]

EXAMPLES
./osio_mqtt_subscriber.py -c | ./node.py -c | ./chroma.py | ./desk.py -v -e

FILES
~/SCS/hue/desk_conf.json

DOCUMENT EXAMPLE - INPUT
{"bri": 254, "transitiontime": 90, "xy": [0.3704, 0.5848]}

SEE ALSO
scs_philips_hue/chroma
scs_philips_hue/desk_conf
"""

import json
import sys
import time

from scs_core.client.network import Network

from scs_core.sys.signalled_exit import SignalledExit

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_desk import CmdDesk

from scs_philips_hue.config.bridge_credentials import BridgeCredentials
from scs_philips_hue.config.desk_conf import DeskConf

from scs_philips_hue.data.light.light_state import LightState

from scs_philips_hue.discovery.discovery import Discovery

from scs_philips_hue.manager.light_manager import LightManager


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    bridge = None
    manager = None
    timeout = False

    indices = {}
    initial_state = {}

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdDesk()

    if cmd.verbose:
        print("desk: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # check...

        if not Network.is_available():
            if cmd.verbose:
                print("desk: waiting for network.", file=sys.stderr)
                sys.stderr.flush()

            Network.wait()


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # DeskConf...
        conf = DeskConf.load(Host, cmd.name)

        if conf is None:
            print("desk: DeskConf not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("desk: %s" % conf, file=sys.stderr)

        # credentials...
        credentials = BridgeCredentials.load(Host)

        if credentials.bridge_id is None:
            print("desk: BridgeCredentials not available")
            exit(1)

        if cmd.verbose:
            print("desk: %s" % credentials, file=sys.stderr)

        # bridge...
        if cmd.verbose:
            print("desk: looking for bridge...", file=sys.stderr)

        discovery = Discovery(Host)
        bridge = discovery.find(credentials)

        if bridge is None:
            print("desk: no bridge matching the stored credentials")
            exit(1)

        if cmd.verbose:
            print("desk: %s" % bridge, file=sys.stderr)

        sys.stderr.flush()

        # manager...
        manager = LightManager(bridge.ip_address, credentials.username)


        # ------------------------------------------------------------------------------------------------------------
        # initialise...

        # signal handler...
        SignalledExit.construct("desk", cmd.verbose)

        # check for bridge availability...
        timeout = time.time() + 10

        while True:
            try:
                manager.find_all()
                break

            except OSError:
                if time.time() > timeout:
                    print("desk: bridge could not be found", file=sys.stderr)
                    exit(1)

                time.sleep(1)
                continue

        # indices...
        for name in conf.lamp_names:
            indices[name] = manager.find_indices_for_name(name)

            if len(indices[name]) == 0:
                print("desk: warning: no light found for name: %s" % name, file=sys.stderr)

            # save initial states...
            for index in indices[name]:
                initial_state[index] = manager.find(index).state        # in case we want to restore these states


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # read stdin...
        for line in sys.stdin:
            sys.stdin.flush()           # remove queue

            datum = line.strip()

            if datum is None:
                break

            if cmd.echo:
                print(datum)
                sys.stdout.flush()

            try:
                jdict = json.loads(datum)
            except ValueError:
                continue

            state = LightState.construct_from_jdict(jdict)

            for name in conf.lamp_names:
                for index in indices[name]:

                    try:
                        response = manager.set_state(index, state)

                        if cmd.verbose:
                            print("desk: %s" % response, file=sys.stderr)
                            sys.stderr.flush()

                    except ConnectionResetError as ex:
                        print("desk: %s: %s" % (ex.__class__.__name__, ex), file=sys.stderr)
                        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except TimeoutError:
        print("desk: Timeout", file=sys.stderr)

    except (KeyboardInterrupt, SystemExit):
        pass

    finally:
        if cmd.verbose:
            print("desk: finishing", file=sys.stderr)

        if manager is not None:
            for index, state in initial_state.items():
                response = manager.set_state(index, LightState.white())     # restore to white

                if cmd.verbose:
                    print("desk: %s" % response, file=sys.stderr)
                    sys.stderr.flush()
