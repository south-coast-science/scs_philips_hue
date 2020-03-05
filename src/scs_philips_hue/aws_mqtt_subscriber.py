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
"""

import sys
import time

from scs_core.aws.client.client_auth import ClientAuth
from scs_core.aws.client.mqtt_client import MQTTClient, MQTTSubscriber

from scs_core.comms.mqtt_conf import MQTTConf
from scs_core.comms.uds_writer import UDSWriter

from scs_core.sys.filesystem import Filesystem
from scs_core.sys.signalled_exit import SignalledExit

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_mqtt_subscriber import CmdMQTTSubscriber

from scs_philips_hue.config.domain_conf import DomainConf

from scs_philips_hue.handler.aws_mqtt_publisher import AWSMQTTPublisher
from scs_philips_hue.handler.aws_mqtt_subscription_handler import AWSMQTTSubscriptionHandler
from scs_philips_hue.handler.mqtt_reporter import MQTTReporter


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    conf = None
    source = None
    reporter = None
    publisher = None
    sub_comms = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdMQTTSubscriber()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("aws_mqtt_subscriber: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # MQTTConf
        conf = MQTTConf.load(Host)

        if cmd.verbose:
            print("aws_mqtt_subscriber: conf: %s" % conf, file=sys.stderr)

        # ClientAuth...
        auth = ClientAuth.load(Host)

        if auth is None:
            print("aws_mqtt_subscriber: ClientAuth not available.", file=sys.stderr)
            exit(1)

        # reporter...
        reporter = MQTTReporter(cmd.verbose)

        # DomainConf...
        if cmd.use_domain_conf:
            domain = DomainConf.load(Host)
            topic_path = domain.topic_path

            if domain is None:
                print("aws_mqtt_subscriber: Domain not available.", file=sys.stderr)
                exit(1)

            if cmd.verbose:
                print("aws_mqtt_subscriber: %s" % domain, file=sys.stderr)
        else:
            topic_path = cmd.topic_path

        # writer...
        sub_comms = UDSWriter(cmd.uds_sub)

        # subscriber...
        handler = AWSMQTTSubscriptionHandler(reporter, sub_comms, False)
        subscriber = MQTTSubscriber(topic_path, handler.handle)

        # client...
        client = MQTTClient(subscriber)
        publisher = AWSMQTTPublisher(conf, auth, client, reporter)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # signal handler...
        SignalledExit.construct("aws_mqtt_subscriber", cmd.verbose)

        # client...
        publisher.connect()

        while True:
            time.sleep(1.0)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except ConnectionError as ex:
        print("aws_mqtt_subscriber: %s" % ex, file=sys.stderr)

    except (KeyboardInterrupt, SystemExit):
        pass

    finally:
        if cmd and cmd.verbose:
            print("aws_mqtt_subscriber: finishing", file=sys.stderr)

        if source:
            source.close()

        if publisher:
            publisher.disconnect()

        if sub_comms:
            sub_comms.close()

        if conf:
            Filesystem.rm(conf.report_file)

        if reporter:
            reporter.print("finished")
