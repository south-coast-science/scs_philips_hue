#!/usr/bin/env python3

"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./osio_mqtt_client.py /orgs/south-coast-science-demo/brighton/loc/1/particulates | \
./node.py /orgs/south-coast-science-demo/brighton/loc/1/particulates.val.pm10 | \
./chroma.py -d 0.0 50.0 -r G R -b 128 -t 9.0 -v | \
./light.py -r 1
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_philips_hue.cmd.cmd_chroma import CmdChroma

from scs_philips_hue.data.light.chroma import ChromaSegment
from scs_philips_hue.data.light.light_state import LightState


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdChroma()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # chromaticity segment...
        segment = ChromaSegment(cmd.range_min_chroma(), cmd.range_max_chroma())

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

            value = cmd.domain_min if value < cmd.domain_min else value
            value = cmd.domain_max if value > cmd.domain_max else value

            intermediate = (value - cmd.domain_min) / (cmd.domain_max - cmd.domain_min)

            chroma = segment.interpolate(intermediate)
            state = LightState(bri=cmd.brightness, xy=chroma, transition_time=cmd.transition_time)

            print(JSONify.dumps(state))
            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("chroma: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)
