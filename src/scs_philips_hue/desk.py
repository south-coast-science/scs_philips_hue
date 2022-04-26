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
import time

from scs_core.client.network import Network

from scs_core.sys.logging import Logging
from scs_core.sys.signalled_exit import SignalledExit

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_desk import CmdDesk

from scs_philips_hue.config.bridge_address import BridgeAddress
from scs_philips_hue.config.bridge_credentials import BridgeCredentials
from scs_philips_hue.config.desk_conf import DeskConfSet

from scs_philips_hue.data.light.light_state import LightState

from scs_philips_hue.discovery.discovery import Discovery

from scs_philips_hue.manager.light_manager import LightManager


# TODO: scs_core.client.resource_unavailable_exception.ResourceUnavailableException - find the bridge again
# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    address = None
    bridge = None
    manager = None
    timeout = False

    indices = {}
    initial_state = {}

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
        desk_confs = DeskConfSet.load(Host, cmd.name)

        if desk_confs is None:
            logger.error("DeskConfSet not available.")
            exit(1)

        logger.info(desk_confs)

        # credentials...
        credentials = BridgeCredentials.load(Host)

        if credentials.bridge_id is None:
            logger.error("BridgeCredentials not available")
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
                logger.error("no bridge matching the stored credentials")
                exit(1)

            logger.info(bridge)
            ip_address = bridge.ip_address

        # manager...
        manager = LightManager(ip_address, credentials.username)


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
                    logger.error("bridge could not be found")
                    exit(1)

                time.sleep(1)
                continue

        # indices...
        for desk_conf in desk_confs.confs.values():
            for name in desk_conf.lamp_names:
                indices[name] = manager.find_indices_for_name(name)

                if len(indices[name]) == 0:
                    logger.error("warning: no light found for name: %s" % name)

                # save initial states...
                for index in indices[name]:
                    initial_state[index] = manager.find(index).state        # in case we want to restore these states


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

            for name, desk_conf in desk_confs.confs.items():
                if name not in datum:
                    continue

                state = LightState.construct_from_jdict(datum[name])

                for lamp_name in desk_conf.lamp_names:
                    for index in indices[lamp_name]:

                        try:
                            response = manager.set_state(index, state)
                            logger.info(response)

                        except ConnectionResetError as ex:
                            logger.error("%s: %s" % (ex.__class__.__name__, ex))
                            sys.stderr.flush()

                break


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except TimeoutError:
        logger.error("Timeout")

    except SystemExit:
        pass

    except KeyboardInterrupt:
        print(file=sys.stderr)

    finally:
        logger.info("finishing")

        if manager is not None:
            for index, state in initial_state.items():
                response = manager.set_state(index, LightState.white())     # restore to white
                logger.info(response)
