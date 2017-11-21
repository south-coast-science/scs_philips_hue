#!/usr/bin/env python3

"""
Created on 23 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

WARNING: only one MQTT client should run at any one time, per TCP/IP host.

Requires APIAuth and ClientAuth documents.

command line example:
./osio_mqtt_subscriber.py /orgs/south-coast-science-demo/brighton/loc/1/particulates
"""

import sys
import time

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.client.client_auth import ClientAuth
from scs_core.osio.manager.topic_manager import TopicManager

from scs_core.sys.exception_report import ExceptionReport

from scs_host.client.http_client import HTTPClient
from scs_host.client.mqtt_client import MQTTClient, MQTTSubscriber

from scs_host.comms.domain_socket import DomainSocket
from scs_host.comms.stdio import StdIO

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_mqtt_subscriber import CmdMQTTSubscriber


# TODO: remove pub code

# --------------------------------------------------------------------------------------------------------------------
# subscription handler...

class OSIOMQTTHandler(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, comms, echo, verbose):
        """
        Constructor
        """
        self.__comms = comms

        self.__echo = echo
        self.__verbose = verbose


    # ----------------------------------------------------------------------------------------------------------------

    def handle(self, pub):
        try:
            self.__comms.connect()
            self.__comms.write(JSONify.dumps(pub), False)

        except ConnectionRefusedError:
            if self.__verbose:
                print("OSIOMQTTHandler: connection refused for %s" % self.__comms.address, file=sys.stderr)
                sys.stderr.flush()

        finally:
            self.__comms.close()

        if self.__echo:
            print(JSONify.dumps(pub))
            sys.stdout.flush()

        if self.__verbose:
            print("received: %s" % JSONify.dumps(pub), file=sys.stderr)
            sys.stderr.flush()


    def print_status(self, status):
        if not self.__verbose:
            return

        now = LocalizedDatetime.now()
        print("%s:         mqtt: %s" % (now.as_iso8601(), status), file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OSIOMQTTHandler:{comms:%s, echo:%s, verbose:%s}" % \
               (self.__comms, self.__echo, self.__verbose)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    client = None


    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdMQTTSubscriber()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # APIAuth...
        api_auth = APIAuth.load(Host)

        if api_auth is None:
            print("APIAuth not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print(api_auth, file=sys.stderr)

        # ClientAuth...
        client_auth = ClientAuth.load(Host)

        if client_auth is None:
            print("ClientAuth not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print(client_auth, file=sys.stderr)

        # manager...
        manager = TopicManager(HTTPClient(), api_auth.api_key)

        # check topics...
        unavailable = False
        for subscription in cmd.subscriptions:
            if not manager.find(subscription.topic):
                print("Topic not available: %s" % subscription[0], file=sys.stderr)
                unavailable = True

        if unavailable:
            exit(1)

        # subscribers...
        subscribers = []

        for subscription in cmd.subscriptions:
            sub_comms = DomainSocket(subscription.address) if subscription.address else StdIO()

            # handler...
            handler = OSIOMQTTHandler(sub_comms, cmd.echo, cmd.verbose)

            if cmd.verbose:
                print(handler, file=sys.stderr)
                sys.stderr.flush()

            subscribers.append(MQTTSubscriber(subscription.topic, handler.handle))

        # client...
        client = MQTTClient(*subscribers)
        client.connect(ClientAuth.MQTT_HOST, client_auth.client_id, client_auth.user_id, client_auth.client_password)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # just join subscribers
        while True:
            time.sleep(1)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("osio_mqtt_client: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        if client:
            client.disconnect()
