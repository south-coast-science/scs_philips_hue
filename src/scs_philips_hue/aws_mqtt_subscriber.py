#!/usr/bin/env python3

"""
Created on 4 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The aws_mqtt_subscriber utility is used to obtain live data from an Amazon Web Services (AWS) messaging topic. The topic
path can be specified either on the command line, or by referencing the domain_conf.json document.

The aws_mqtt_subscriber passes subscribed data to stdout. Data is wrapped in a JSON document that uses the topic
path as a field name, thus identifying which topic the data was gained from.

In order to operate, the appropriate AWS certificates must be installed in a ~/SCS/aws/certs directory, and the
certificate and API auth specified in the aws_api_auth.json and client_credentials.json documents.

WARNING: only one MQTT client should run at any one time, per TCP/IP host.

EXAMPLES
./aws_mqtt_subscriber.py -c | ./node.py -c | ./chroma.py | ./desk.py -v -e

FILES
~/SCS/aws/aws_api_auth.json
~/SCS/aws/client_credentials.json
~/SCS/aws/endpoint.json
~/SCS/hue/domain_conf.json

DOCUMENT EXAMPLE
{"south-coast-science-dev/production-test/loc/1/climate":
{"tag": "scs-be2-2", "rec": "2018-03-17T09:18:07.681+00:00", "val": {"hmd": 46.7, "tmp": 23.9}}}

SEE ALSO
scs_philips_hue/osio_mqtt_subscriber.py
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

from scs_host.comms.stdio import StdIO

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_mqtt_subscriber import CmdMQTTSubscriber
from scs_philips_hue.config.domain_conf import DomainConf


# --------------------------------------------------------------------------------------------------------------------
# subscription handler...

class AWSMQTTHandler(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, comms=None, verbose=False):
        """
        Constructor
        """
        self.__comms = comms
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

        if self.__verbose:
            print("received: %s" % JSONify.dumps(pub), file=sys.stderr)
            sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AWSMQTTHandler:{comms:%s, verbose:%s}" % (self.__comms, self.__verbose)


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

        if cmd.verbose:
            print(endpoint, file=sys.stderr)

        # endpoint...
        credentials = ClientCredentials.load(Host)

        if credentials is None:
            print("ClientCredentials not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print(credentials, file=sys.stderr)

        # DomainConf...
        if cmd.use_domain_conf:
            domain = DomainConf.load(Host)
            topic_path = domain.topic_path

            if domain is None:
                print("Domain not available.", file=sys.stderr)
                exit(1)

            if cmd.verbose:
                print(domain, file=sys.stderr)
        else:
            topic_path = cmd.topic_path

        # subscriber...
        handler = AWSMQTTHandler(StdIO(), cmd.verbose)
        subscriber = MQTTSubscriber(topic_path, handler.handle)

        # client...
        client = MQTTClient(subscriber)

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
