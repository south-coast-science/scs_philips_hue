#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

DESCRIPTION
The chroma_conf utility is used to specify the parameters of a mapping from environmental data domain values to
locations in a chromaticity space. In addition to chromaticity mapping, the configuration includes lamp brightness and
transition time.

A chromaticity chart is available at: https://developers.meethue.com/documentation/core-concepts

The mapping is specified as a start point - a minimum - followed by one or more intervals. When a chroma_conf
configuration is first created, a minimum and one interval must be specified. Subsequent intervals may be added, one
at a time. Intervals are stored in ascending order of their domain value.

The chroma_conf.json document managed by the chroma_conf utility is used by chroma.py

SYNOPSIS
chroma_conf.py [-m DOMAIN_MIN CHR_X CHR_Y] [-i DOMAIN_MAX CHR_X CHR_Y] [-b BRIGHTNESS] [-t TRANSITION] [-v]

EXAMPLES
./chroma_conf.py -m 0 0.08 0.84 -i 100 0.74 0.26 -b 254 -t 9

FILES
~/SCS/hue/chroma_conf.json

DOCUMENT EXAMPLE
{"min": {"domain-min": 0, "range-min": [0.08, 0.84]}, "intervals": [{"domain-max": 100, "range-max": [0.74, 0.26]}],
"brightness": 128, "transition-time": 9}

SEE ALSO
scs_philips_hue/chroma

RESOURCES
https://en.wikipedia.org/wiki/Chromaticity
https://developers.meethue.com/documentation/core-concepts
"""

import sys

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_chroma_conf import CmdChromaConf
from scs_philips_hue.config.chroma_conf import ChromaConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdChromaConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("chroma_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # ChromaConf...
    conf = ChromaConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None:
            if not cmd.is_complete():
                print("chroma_conf: no configuration is stored. You must therefore set all fields:", file=sys.stderr)
                cmd.print_help(sys.stderr)
                exit(1)

            conf = ChromaConf(cmd.minimum, [cmd.insert_interval], cmd.brightness, cmd.transition_time)

        else:
            minimum = conf.minimum if cmd.minimum is None else cmd.minimum

            if cmd.insert_interval is None:
                intervals = conf.intervals

            else:
                conf.insert_interval(cmd.insert_interval)
                intervals = conf.intervals

            brightness = conf.brightness if cmd.brightness is None else cmd.brightness
            transition_time = conf.transition_time if cmd.transition_time is None else cmd.transition_time

            conf = ChromaConf(minimum, intervals, brightness, transition_time)

        conf.save(Host)

    if cmd.delete_interval:
        if conf is None:
            print("chroma_conf: There are no intervals to be deleted.", file=sys.stderr)
            exit(1)

        if len(conf) < 2:
            print("chroma_conf: There must be at least one interval.", file=sys.stderr)
            exit(1)

        if not conf.has_interval(cmd.delete_interval):
            print("chroma_conf: No interval exists with that domain value.", file=sys.stderr)
            exit(1)

        conf.remove_interval(cmd.delete_interval)
        conf.save(Host)

    if conf:
        print(JSONify.dumps(conf))
