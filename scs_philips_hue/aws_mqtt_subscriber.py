#!/usr/bin/env python3

"""
Created on 4 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

WARNING: only one MQTT client should run at any one time, per TCP/IP host.

Requires Endpoint and ClientCredentials documents.

command line example:
./gases_sampler.py -i2 | \
    ./aws_topic_publisher.py -t south-coast-science-dev/development/loc/3/gases | \
    ./aws_mqtt_subscriber.py -s -e
"""

import json
import sys
import time

from collections import OrderedDict

from scs_core.aws.client.mqtt_client import MQTTClient, MQTTSubscriber
from scs_core.aws.client.client_credentials import ClientCredentials
from scs_core.aws.service.endpoint import Endpoint

from scs_core.data.json import JSONify
from scs_core.data.publication import Publication

from scs_core.sys.exception_report import ExceptionReport

from scs_host.comms.domain_socket import DomainSocket
from scs_host.comms.stdio import StdIO

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_mqtt_subscriber import CmdMQTTSubscriber


# --------------------------------------------------------------------------------------------------------------------
# subscription handler...

class AWSMQTTHandler(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, comms=None, echo=False, verbose=False):
        """
        Constructor
        """
        self.__comms = comms

        self.__echo = echo
        self.__verbose = verbose


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyUnusedLocal,PyShadowingNames
    def handle(self, client, userdata, message):
        payload = json.loads(message.payload.decode(), object_pairs_hook=OrderedDict)

        pub = Publication(message.topic, payload)

        try:
            self.__comms.connect()
            self.__comms.write(JSONify.dumps(pub), False)

        except ConnectionRefusedError:
            if self.__verbose:
                print("AWSMQTTHandler: connection refused for %s" % self.__comms.address, file=sys.stderr)
                sys.stderr.flush()

        finally:
            self.__comms.close()

        if self.__echo:
            print(JSONify.dumps(pub))
            sys.stdout.flush()

        if self.__verbose:
            print("received: %s" % JSONify.dumps(pub), file=sys.stderr)
            sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AWSMQTTHandler:{comms:%s, echo:%s, verbose:%s}" % \
               (self.__comms, self.__echo, self.__verbose)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    client = None
    pub_comms = None


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

        # endpoint...
        endpoint = Endpoint.load(Host)

        if endpoint is None:
            print("Endpoint config not available.", file=sys.stderr)
            exit(1)

        # endpoint...
        credentials = ClientCredentials.load(Host)

        if credentials is None:
            print("ClientCredentials not available.", file=sys.stderr)
            exit(1)

        # subscribers...
        subscribers = []

        for subscription in cmd.subscriptions:
            sub_comms = DomainSocket(subscription.address) if subscription.address else StdIO()

            # handler...
            handler = AWSMQTTHandler(sub_comms, cmd.echo, cmd.verbose)

            if cmd.verbose:
                print(handler, file=sys.stderr)

            subscribers.append(MQTTSubscriber(subscription.topic, handler.handle))

        # client...
        client = MQTTClient(*subscribers)

        if cmd.verbose:
            print(client, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        client.connect(endpoint, credentials)

        # just join subscribers
        while True:
            time.sleep(1)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("aws_mqtt_client: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        if client:
            client.disconnect()
