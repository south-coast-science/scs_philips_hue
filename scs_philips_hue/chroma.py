#!/usr/bin/env python3

"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./osio_mqtt_client.py /orgs/south-coast-science-demo/brighton/loc/1/particulates | \
./node.py /orgs/south-coast-science-demo/brighton/loc/1/particulates.val.pm10 | \
./chroma.py -m50.0 -zG -uR -t9.0 -v
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

    manager = None
    initial = None

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
        segment = ChromaSegment(cmd.zero_chroma(), cmd.upper_chroma())

        if cmd.verbose:
            print(segment, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # dim the lights...
        dark = LightState(on=True, bri=0, transition_time=cmd.transition_time / 2.0)

        print(JSONify.dumps(dark))
        sys.stdout.flush()

        # samples...
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

            proportion = value / cmd.max_value
            intermediate = 0.0 if proportion < 0.0 else proportion
            intermediate = 1.0 if proportion > 1.0 else proportion

            point = segment.interpolate(intermediate)
            state = LightState(bri=cmd.brightness, xy=point, transition_time=cmd.transition_time)

            print(JSONify.dumps(state))
            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("chroma: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)
