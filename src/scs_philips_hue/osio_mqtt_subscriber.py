#!/usr/bin/env python3

"""
Created on 23 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The osio_mqtt_subscriber utility is used to obtain live data from an OpenSensors messaging topic. The topic
path can be specified either on the command line, or by referencing the domain_conf.json document.

The osio_mqtt_subscriber passes subscribed data to stdout. Data is wrapped in a JSON document that uses the topic
path as a field name, thus identifying which topic the data was gained from.

In order to operate, the API auth and client auth must be specified in the aws_api_auth.json and
client_credentials.json documents.

WARNING: only one MQTT client should run at any one time, per TCP/IP host.

SYNOPSIS
osio_mqtt_subscriber.py {-c | -t TOPIC_PATH } [-v]

EXAMPLES
./osio_mqtt_subscriber.py -c | ./node.py -c | ./chroma.py | ./desk.py -v -e

FILES
~/SCS/hue/domain_conf.json
~/SCS/osio/osio_api_auth.json
~/SCS/osio/osio_client_auth.json

DOCUMENT EXAMPLE
{"/south-coast-science-dev/production-test/loc/1/climate":
{"tag": "scs-be2-2", "rec": "2018-03-17T09:18:07.681+00:00", "val": {"hmd": 46.7, "tmp": 23.9}}}

SEE ALSO
scs_philips_hue/domain_conf
scs_philips_hue/osio_api_auth
scs_philips_hue/osio_client_auth
scs_philips_hue/aws_mqtt_subscriber
"""

import sys
import time

from scs_core.data.json import JSONify

from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.client.client_auth import ClientAuth
from scs_core.osio.manager.topic_manager import TopicManager

from scs_core.sys.exception_report import ExceptionReport

from scs_host.client.http_client import HTTPClient
from scs_host.client.mqtt_client import MQTTClient, MQTTSubscriber

from scs_host.comms.stdio import StdIO

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_mqtt_subscriber import CmdMQTTSubscriber
from scs_philips_hue.config.domain_conf import DomainConf


# --------------------------------------------------------------------------------------------------------------------
# subscription handler...

class OSIOMQTTHandler(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, comms, verbose):
        """
        Constructor
        """
        self.__comms = comms
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

        if self.__verbose:
            print("osio_mqtt_subscriber: received: %s" % JSONify.dumps(pub), file=sys.stderr)
            sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OSIOMQTTHandler:{comms:%s, verbose:%s}" %  (self.__comms, self.__verbose)


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
            print("osio_mqtt_subscriber: APIAuth not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print(api_auth, file=sys.stderr)

        # ClientAuth...
        client_auth = ClientAuth.load(Host)

        if client_auth is None:
            print("osio_mqtt_subscriber: ClientAuth not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print(client_auth, file=sys.stderr)

        # DomainConf...
        if cmd.use_domain_conf:
            domain = DomainConf.load(Host)
            topic_path = domain.topic_path

            if domain is None:
                print("osio_mqtt_subscriber: Domain not available.", file=sys.stderr)
                exit(1)

            if cmd.verbose:
                print(domain, file=sys.stderr)
        else:
            topic_path = cmd.topic_path

        # manager...
        manager = TopicManager(HTTPClient(), api_auth.api_key)

        # check topics...
        if not manager.find(topic_path):
            print("osio_mqtt_subscriber: Topic not available: %s" % topic_path, file=sys.stderr)
            exit(1)

        # subscribers...
        handler = OSIOMQTTHandler(StdIO(), cmd.verbose)
        subscriber = MQTTSubscriber(topic_path, handler.handle)

        # client...
        client = MQTTClient(subscriber)
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
            print("osio_mqtt_subscriber: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        if client:
            client.disconnect()
