#!/usr/bin/env python3

"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The chroma utility is used to map environmental data domain values to chromaticity locations. Input data is received
from stdin, and is interpreted as a float value. The mapped value is written to stdout in the form of a JSON
scs_philips_hue.data.light.LightState document.

The chroma utility requires the chroma_conf.json document, specifying the parameters of the mapping.

SYNOPSIS
chroma.py [-v]

EXAMPLES
./osio_mqtt_subscriber.py -c | ./node.py -c | ./chroma.py | ./desk.py -v -e

FILES
~/SCS/hue/chroma_conf.json

DOCUMENT EXAMPLE - OUTPUT
{"bri": 254, "transitiontime": 90, "xy": [0.3704, 0.5848]}

SEE ALSO
scs_philips_hue/chroma_conf
scs_philips_hue/desk

RESOURCES
https://en.wikipedia.org/wiki/Chromaticity
https://developers.meethue.com/documentation/core-concepts
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_simple import CmdSimple

from scs_philips_hue.config.chroma_conf import ChromaConf

from scs_philips_hue.data.light.chroma import ChromaSegment
from scs_philips_hue.data.light.light_state import LightState


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSimple()

    if cmd.verbose:
        print("chroma: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # ChromaConf...
        conf = ChromaConf.load(Host)

        if conf is None:
            print("chroma: ChromaConf not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("chroma: %s" % conf, file=sys.stderr)

        domain_min = conf.domain_min
        domain_max = conf.domain_max

        # chromaticity segment...
        segment = ChromaSegment(conf.range_min, conf.range_max)

        if cmd.verbose:
            print("chroma: %s" % segment, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # read stdin...
        for line in sys.stdin:
            datum = line.strip()

            if datum is None:
                break

            if cmd.verbose:
                print("chroma: %s" % datum, file=sys.stderr)
                sys.stderr.flush()

            try:
                value = float(datum)
            except ValueError:
                continue

            # clip...
            domain_value = domain_min if value < domain_min else value
            domain_value = domain_max if value > domain_max else value

            # interpolate...
            intermediate = (domain_value - domain_min) / (domain_max - domain_min)

            chroma = segment.interpolate(intermediate)
            state = LightState(bri=conf.brightness, xy=chroma, transition_time=conf.transition_time)

            print(JSONify.dumps(state))
            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("chroma: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)
