#!/usr/bin/env python3

"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

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
from scs_core.sys.signalled_exit import SignalledExit

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_chroma import CmdChroma

from scs_philips_hue.config.chroma_conf import ChromaConf

from scs_philips_hue.data.light.chroma import ChromaPath
from scs_philips_hue.data.light.light_state import LightState


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdChroma()

    if cmd.verbose:
        print("chroma: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # ChromaConf...
        conf = ChromaConf.load_from_file(cmd.file) if cmd.file else ChromaConf.load(Host)

        if conf is None:
            print("chroma: ChromaConf not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            print("chroma: %s" % conf, file=sys.stderr)

        # chromaticity path...
        path = ChromaPath.construct(conf.minimum, conf.intervals)

        if cmd.verbose:
            print("chroma: %s" % path, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # signal handler...
        SignalledExit.construct("chroma", cmd.verbose)

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

            # interpolate...
            chroma = path.interpolate(value)
            state = LightState(bri=conf.brightness, xy=chroma, transition_time=conf.transition_time)

            print(JSONify.dumps(state))
            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except (KeyboardInterrupt, SystemExit):
        pass

    finally:
        if cmd and cmd.verbose:
            print("chroma: finishing", file=sys.stderr)
