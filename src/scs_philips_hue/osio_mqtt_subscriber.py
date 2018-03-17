#!/usr/bin/env python3

"""
Created on 23 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

WARNING: only one MQTT client should run at any one time, per TCP/IP host.

Requires APIAuth and ClientAuth documents.
May require DomainConf document.

command line example:
./osio_mqtt_subscriber.py -v
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

        # manager...
        manager = TopicManager(HTTPClient(), api_auth.api_key)

        # check topics...
        if not manager.find(topic_path):
            print("Topic not available: %s" % topic_path, file=sys.stderr)
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
