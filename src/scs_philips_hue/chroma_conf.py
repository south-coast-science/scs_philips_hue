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

The chroma_conf utility works in conjunction with a chroma path: the path specifies two or more ordered points in
chroma space, indicating a progression through different colours as a domain value changes. The chroma path
specifies the shape of this route, the chroma conf specifies the minimum and maximum domain values associated
with a progression though the chroma space.

Note that - currently - there is no command line utility to edit chroma paths, and only default paths can be used.

SYNOPSIS
chroma_conf.py [-p PATH_NAME] [-l DOMAIN_MIN] [-u DOMAIN_MAX] [-b BRIGHTNESS] [-t TRANSITION] [-v]

EXAMPLES
./chroma_conf.py -p risk-level -l 5 -u 30 -b 254 -t 9

FILES
~/SCS/hue/chroma_conf.json

DOCUMENT EXAMPLE
{"path-name": "risk-level", "domain-min": 5, "domain-max": 30, "brightness": 254, "transition-time": 9}

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
                print("chroma_conf: no configuration is stored - you must therefore set all fields.", file=sys.stderr)
                cmd.print_help(sys.stderr)
                exit(2)

            conf = ChromaConf(cmd.path_name, cmd.domain_min, cmd.domain_max, cmd.brightness, cmd.transition_time)

        else:
            path_name = conf.path_name if cmd.path_name is None else cmd.path_name
            domain_min = conf.domain_min if cmd.domain_min is None else cmd.domain_min
            domain_max = conf.domain_max if cmd.domain_max is None else cmd.domain_max
            brightness = conf.brightness if cmd.brightness is None else cmd.brightness
            transition_time = conf.transition_time if cmd.transition_time is None else cmd.transition_time

            conf = ChromaConf(path_name, domain_min, domain_max, brightness, transition_time)

        conf.save(Host)

    if conf:
        print(JSONify.dumps(conf))
