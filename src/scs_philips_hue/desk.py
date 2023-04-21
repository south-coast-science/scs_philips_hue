#!/usr/bin/env python3

"""
Created on 25 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

DESCRIPTION
The desk utility (a lighting control desk) is used to drive the Philips Hue bridge device. Input data is received
from stdin, and is interpreted as a scs_philips_hue.data.light.LightState document.

If a bridge address has been stored, this is used to find the bridge. Otherwise a UPnP or IP scan is attempted.

In verbose mode, the desk utility provides a detailed report on the command outcome to stderr.

The desk utility requires the desk_conf.json document, specifying which light(s) should receive the LightState
command.

Note: this utility waits forever for a network connection and domain name server.

SYNOPSIS
desk.py [-n NAME] [-e] [-v]

EXAMPLES
./aws_mqtt_subscriber.py -vc | ./node.py -vc | ./chroma.py -v | ./desk.py -ve

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
import termios

from scs_core.client.network import Network

from scs_core.sys.logging import Logging
from scs_core.sys.signalled_exit import SignalledExit

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_desk import CmdDesk

from scs_philips_hue.config.bridge_credentials import BridgeCredentialsSet
from scs_philips_hue.config.desk_conf import DeskConfSet

from scs_philips_hue.data.light.light_catalogue import LightCatalogue
from scs_philips_hue.data.light.light_state import LightState

from scs_philips_hue.manager.bridge_builder import BridgeBuilder
from scs_philips_hue.manager.light_manager import LightManager


# TODO: scs_core.client.resource_unavailable_exception.ResourceUnavailableException - find the bridge again
# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    light_managers = {}
    light_catalogue = LightCatalogue({})

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdDesk()

    Logging.config('desk', verbose=cmd.verbose)
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

        # DeskConf...
        desk_conf_set = DeskConfSet.load(Host, cmd.name)

        if desk_conf_set is None:
            logger.error("DeskConfSet not available.")
            exit(1)

        logger.info(desk_conf_set)

        # BridgeCredentials...
        credentials_set = BridgeCredentialsSet.load(Host, skeleton=True)

        if len(credentials_set) < 1:
            logger.error("BridgeCredentials not available.")
            exit(1)

        # Managers...
        bridge_managers = BridgeBuilder(Host).construct_all(credentials_set)
        light_managers = LightManager.construct_all(bridge_managers)

        # LightCatalogue...
        light_catalogue = LightCatalogue.construct(light_managers)


        # ------------------------------------------------------------------------------------------------------------
        # initialise...

        # signal handler...
        SignalledExit.construct("desk", cmd.verbose)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # read stdin...
        for line in sys.stdin:
            try:
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)           # flush stdin
            except termios.error:
                pass

            if line is None:
                break

            if cmd.echo:
                print(line.strip())
                sys.stdout.flush()

            try:
                datum = json.loads(line)
            except ValueError:
                continue

            for channel in datum.keys():
                if channel not in desk_conf_set:
                    logger.info("encountered unsupported channel: %s" % channel)
                    exit(1)

                state = LightState.construct_from_jdict(datum[channel])

                for light_name in desk_conf_set.conf(channel).lamp_names:
                    if light_name not in light_catalogue:
                        logger.info("encountered unknown light name: %s" % light_name)
                        exit(1)

                    light = light_catalogue.light(light_name)
                    manager = light_managers[light.bridge_name]

                    try:
                        response = manager.set_state(light.index, state)
                        logger.info(response)

                    except ConnectionResetError as ex:
                        logger.error(repr(ex))
                        exit(1)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        print(file=sys.stderr)

    except TimeoutError:
        logger.error("Timeout")

    except SystemExit:
        pass

    finally:
        logger.info("finishing")

        for light in light_catalogue.sorted_entries.values():
            manager = light_managers[light.bridge_name]
            response = manager.set_state(light.index, LightState.white())
            logger.info(response)
