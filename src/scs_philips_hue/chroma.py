#!/usr/bin/env python3

"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://en.wikipedia.org/wiki/Chromaticity
https://developers.meethue.com/documentation/core-concepts

command line example:
./osio_mqtt_subscriber.py /orgs/south-coast-science-demo/brighton/loc/1/particulates | \
    ./node.py /orgs/south-coast-science-demo/brighton/loc/1/particulates.val.pm2p5 | \
    ./chroma_conf.py -d 0 50 -r G R -t 9.0 -b 128 -v
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
        print(cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # ChromaConf...
        conf = ChromaConf.load(Host)

        if conf is None:
            print("ChromaConf not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print(conf, file=sys.stderr)

        domain_min = conf.domain_min
        domain_max = conf.domain_max

        # chromaticity segment...
        segment = ChromaSegment(conf.range_min, conf.range_max)

        if cmd.verbose:
            print(segment, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # read stdin...
        for line in sys.stdin:
            datum = line.strip()

            if datum is None:
                break

            if cmd.verbose:
                print(datum, file=sys.stderr)
                sys.stderr.flush()

            try:
                value = float(datum)
            except ValueError:
                continue

            value = domain_min if value < domain_min else value
            value = domain_max if value > domain_max else value

            intermediate = (value - domain_min) / (domain_max - domain_min)

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
