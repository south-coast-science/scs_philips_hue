#!/usr/bin/env python3

"""
Created on 11 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The node utility is used to extract a node within a JSON document. Data is presented as a sequence of documents on
stdin, the node is passed to stdout. The extracted node may be a leaf node or an internal node.

The node path can be specified either on the command line, or by referencing the domain_conf.json document.
The node utility may be set to either ignore documents that do not contain the specified node, or to terminate if the
node is not present.

SYNOPSIS
node.py {-c | -t TOPIC_PATH } [-i] [-v]

EXAMPLES
./osio_mqtt_subscriber.py -c | ./node.py -c | ./chroma.py | ./desk.py -v -e

FILES
~/SCS/hue/domain_conf.json

SEE ALSO
scs_philips_hue/aws_mqtt_subscriber
scs_philips_hue/osio_mqtt_subscriber
scs_philips_hue/domain_conf
"""

import sys

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_node import CmdNode
from scs_philips_hue.config.domain_conf import DomainConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNode()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("node: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # DomainConf...
        if cmd.use_domain_conf:
            domain = DomainConf.load(Host)
            topic_path = '.'.join((domain.topic_path, domain.document_node))

            if domain is None:
                print("node: Domain not available.", file=sys.stderr)
                exit(1)

            if cmd.verbose:
                print("node: %s" % domain, file=sys.stderr)
        else:
            topic_path = cmd.topic_path


        # ------------------------------------------------------------------------------------------------------------
        # run...

        node = None

        for line in sys.stdin:
            datum = PathDict.construct_from_jstr(line)

            if datum is None:
                continue

            if cmd.ignore and not datum.has_path(topic_path):
                continue

            try:
                node = datum.node(topic_path)

            except KeyError as ex:
                print("node: KeyError: %s datum:%s" % (ex, datum), file=sys.stderr)
                sys.stderr.flush()
                continue

            print(JSONify.dumps(node))
            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("node: KeyboardInterrupt", file=sys.stderr)
