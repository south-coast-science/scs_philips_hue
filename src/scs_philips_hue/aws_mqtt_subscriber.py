#!/usr/bin/env python3

"""
Created on 4 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

DESCRIPTION
The aws_mqtt_subscriber utility is used to obtain live data from an Amazon Web Services (AWS) messaging topic. The topic
path can be specified either on the command line, or by referencing the domain_conf.json document.

The aws_mqtt_subscriber passes subscribed data to stdout. Data is wrapped in a JSON document that uses the topic
path as a field name, thus identifying which topic the data was gained from.

In order to operate, the appropriate AWS certificates must be installed in a ~/SCS/aws/certs directory, and the
certificate and API auth specified in the aws_api_auth.json and client_credentials.json documents.

WARNING: only one MQTT client should run at any one time, per TCP/IP host.

SYNOPSIS
aws_mqtt_subscriber.py {-c | -t TOPIC_PATH } [-s UDS_SUB] [-v]

EXAMPLES
./aws_mqtt_subscriber.py -c | ./node.py -c | ./chroma.py | ./desk.py -v

FILES
~/SCS/aws/aws_client_auth.json
~/SCS/hue/domain_conf.json

SEE ALSO
scs_philips_hue/aws_client_auth
scs_philips_hue/aws_mqtt_subscriber
scs_philips_hue/domain_conf

BUGS
If the host is multi-homed and a higher-priority connection is lost, the MQTT connection will
not be recovered.
"""

import sys
import time

from scs_core.aws.client.client_auth import ClientAuth
from scs_core.aws.client.mqtt_client import MQTTClient, MQTTSubscriber

from scs_core.client.network import NetworkMonitor

from scs_core.comms.mqtt_conf import MQTTConf
from scs_core.comms.uds_writer import UDSWriter

from scs_core.sys.filesystem import Filesystem
from scs_core.sys.logging import Logging
from scs_core.sys.signalled_exit import SignalledExit

from scs_host.comms.domain_socket import DomainSocket
from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_mqtt_subscriber import CmdMQTTSubscriber

from scs_philips_hue.config.domain_conf import DomainConfSet

from scs_philips_hue.handler.aws_mqtt_subscription_handler import AWSMQTTSubscriptionHandler
from scs_philips_hue.handler.mqtt_reporter import MQTTReporter


# --------------------------------------------------------------------------------------------------------------------

def network_not_available_handler():
    # noinspection PyShadowingNames
    logger = Logging.getLogger()
    logger.error("network loss - attempting to reconnect MQTT client")

    client.disconnect()                                                 # remove dead connection
    connect_client()


def connect_client():
    while True:
        try:
            client.connect(auth, debug=Logging.degugging_on())          # connect when possible
            break
        except OSError:
            time.sleep(10)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    conf = None
    domains = None
    client = None
    reporter = None
    publisher = None
    sub_comms = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdMQTTSubscriber()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    Logging.config('aws_mqtt_subscriber', verbose=cmd.verbose)       # , level=logging.DEBUG  , verbose=cmd.verbose
    logger = Logging.getLogger()

    logger.info(cmd)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # MQTTConf
        conf = MQTTConf.load(Host, skeleton=True)
        logger.info(conf)

        # ClientAuth...
        auth = ClientAuth.load(Host)

        if auth is None:
            logger.error("ClientAuth not available.")
            exit(1)

        # reporter...
        reporter = MQTTReporter(cmd.verbose)

        # DomainConf...
        if cmd.use_domain_conf:
            domains = DomainConfSet.load(Host)

            if domains is None:
                logger.error("DomainConfSet not available.")
                exit(1)

            logger.info(domains)

        else:
            topic_path = cmd.topic_path

        # writer...
        sub_comms = UDSWriter(DomainSocket, cmd.uds_sub)

        # subscriber...
        handler = AWSMQTTSubscriptionHandler(reporter, sub_comms, cmd.echo)

        subscribers = []
        if cmd.use_domain_conf:
            for topic_path in domains.topic_paths():
                subscribers.append(MQTTSubscriber(topic_path, handler.handle))
        else:
            subscribers.append(MQTTSubscriber(cmd.topic_path, handler.handle))

        # client...
        client = MQTTClient(*subscribers)

        # monitor...
        monitor = NetworkMonitor(10, network_not_available_handler)
        logger.info(monitor)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # signal handler...
        SignalledExit.construct("aws_mqtt_subscriber", cmd.verbose)

        # client...
        connect_client()

        # monitor...
        monitor.start()
        monitor.join()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except ConnectionError as ex:
        logger.error(repr(ex))

    except (KeyboardInterrupt, SystemExit):
        pass

    finally:
        logger.info("finishing")

        if client:
            client.disconnect()

        if sub_comms:
            sub_comms.close()

        if conf:
            Filesystem.rm(conf.report_file)

        if reporter:
            reporter.print("finished")
