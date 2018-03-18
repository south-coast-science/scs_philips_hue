#!/usr/bin/env python3

"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The chroma_conf utility is used to specify the parameters of a mapping from environmental data domain values to
chromaticity locations. In addition to chromaticity mapping, the configuration includes lamp brightness and
transition time.

The chroma_conf.json document managed by the chroma_conf utility is used by chroma.py

EXAMPLES
./chroma_conf.py -v -p /orgs/south-coast-science-demo/brighton/loc/1/particulates

FILES
~/SCS/hue/chroma_conf.json

DOCUMENT EXAMPLE
{"domain-min": 0.0, "domain-max": 50.0, "range-min": [0.08, 0.84], "range-max": [0.74, 0.26],
"brightness": 128, "transition-time": 9}

SEE ALSO
scs_philips_hue/chroma.py
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
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # ChromaConf...
    conf = ChromaConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("chroma_conf: no configuration is stored. You must therefore set all fields:", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(1)

        domain_min = conf.domain_min if cmd.domain_min is None else cmd.domain_min
        domain_max = conf.domain_max if cmd.domain_max is None else cmd.domain_max

        range_min = conf.range_min if cmd.range_min is None else cmd.range_min
        range_max = conf.range_max if cmd.range_max is None else cmd.range_max

        brightness = conf.brightness if cmd.brightness is None else cmd.brightness
        transition_time = conf.transition_time if cmd.transition_time is None else cmd.transition_time

        conf = ChromaConf(domain_min, domain_max, range_min, range_max, brightness, transition_time)
        conf.save(Host)

    if cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
