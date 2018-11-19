#!/usr/bin/env python3

"""
Created on 11 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The node utility is used to extract a node from within a JSON document. Data is presented as a sequence of documents on
stdin, and the extracted node is passed to stdout. The extracted node may be a leaf node or an internal node. If no
node path is specified, the whole input document is passed to stdout.

The node utility may be set to either ignore documents that do not contain the specified node, or to terminate if the
node is not present.

By default, output is in the form of a sequence of JSON documents, separated by newlines. If the array (-a) option is
selected, output is in the form of a JSON array - the output opens with a '[' character, documents are separated by
the ',' character, and the output is terminated by a ']' character.

Alternatively, if the node is an array or other iterable type, then it may be output as a sequence (a list of items
separated by newline characters) according to the -s flag.

SYNOPSIS
node.py [-i] [{ -a | -s }] [-v] [PATH]

EXAMPLES
climate_sampler.py -i5 | node.py val

DOCUMENT EXAMPLE - INPUT
{"tag": "scs-ap1-6", "rec": "2018-04-04T14:50:38.394+00:00", "val": {"hmd": 59.7, "tmp": 23.8}}
{"tag": "scs-ap1-6", "rec": "2018-04-04T14:55:38.394+00:00", "val": {"hmd": 59.8, "tmp": 23.9}}

DOCUMENT EXAMPLE - OUTPUT
Default mode:
{"hmd": 59.7, "tmp": 23.8}
{"hmd": 59.8, "tmp": 23.9}

Array mode:
[{"hmd": 59.7, "tmp": 23.8}, {"hmd": 59.8, "tmp": 23.9}]
"""

import sys

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict

from scs_philips_hue.cmd.cmd_node import CmdNode


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
        # run...

        if cmd.array:
            print('[', end='')

        first = True

        for line in sys.stdin:
            datum = PathDict.construct_from_jstr(line)

            if datum is None:
                continue

            if cmd.ignore and not datum.has_path(cmd.path):
                continue

            node = datum.node(cmd.path)
            document = JSONify.dumps(node)

            if cmd.sequence:
                try:
                    for item in node:
                        print(JSONify.dumps(item))
                except TypeError:
                    print(document)

            else:
                if cmd.array:
                    if first:
                        print(document, end='')
                        first = False

                    else:
                        print(", %s" % document, end='')

                else:
                    print(document)

            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("node: KeyboardInterrupt", file=sys.stderr)

    finally:
        if cmd.array:
            print(']')

