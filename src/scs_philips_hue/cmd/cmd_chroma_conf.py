"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"domain-min": 0.0, "domain-max": 50.0, "range-min": [0.08, 0.84], "range-max": [0.74, 0.26],
"brightness": 128, "transition-time": 9}
"""

import optparse

from scs_philips_hue.config.chroma_conf import ChromaConf


# --------------------------------------------------------------------------------------------------------------------

class CmdChromaConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ [-d DOMAIN_MIN DOMAIN_MAX] "
                                                    "[-r { R | G | B | W } { R | G | B | W }] "
                                                    "[-b BRIGHTNESS] [-t TRANSITION] | -x }] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--domain", "-d", type="float", nargs=2, action="store", dest="domain",
                                 help="set domain min and max values")

        self.__parser.add_option("--range", "-r", type="string", nargs=2, action="store", dest="range",
                                 help="set range min and max chromaticity")

        self.__parser.add_option("--bright", "-b", type="int", nargs=1, action="store", dest="brightness",
                                 help="set the lamp brightness (max 254)")

        self.__parser.add_option("--trans", "-t", type="float", nargs=1, action="store", dest="transition_time",
                                 help="set the lamp transition time (seconds)")

        self.__parser.add_option("--delete", "-x", action="store_true", dest="delete",
                                 help="delete the Chroma configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete is not None:
            return False

        if self.__opts.range is not None and self.__opts.range[0] not in ChromaConf.CANONICAL_CHROMAS:
            return False

        if self.__opts.range is not None and self.__opts.range[1] not in ChromaConf.CANONICAL_CHROMAS:
            return False

        if self.__opts.domain is not None and self.domain_min > self.domain_max:
            return None

        if self.brightness is not None and (self.brightness < 0 or self.brightness > 254):
            return False

        return True


    def is_complete(self):
        if self.__opts.domain is None or self.__opts.range is None or \
                self.brightness is None or self.transition_time is None:
            return False

        return True


    def set(self):
        return self.__opts.domain is not None or self.__opts.range is not None or \
               self.brightness is not None or self.transition_time is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def domain_min(self):
        return None if self.__opts.domain is None else self.__opts.domain[0]


    @property
    def domain_max(self):
        return None if self.__opts.domain is None else self.__opts.domain[1]


    @property
    def range_min(self):
        return None if self.__opts.range is None else ChromaConf.CANONICAL_CHROMAS[self.__opts.range[0]]


    @property
    def range_max(self):
        return None if self.__opts.range is None else ChromaConf.CANONICAL_CHROMAS[self.__opts.range[1]]


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def brightness(self):
        return self.__opts.brightness


    @property
    def transition_time(self):
        return self.__opts.transition_time


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def args(self):
        return self.__args


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdChromaConf:{domain:%s, range:%s, brightness:%s, transition_time:%s, " \
               "delete:%s, verbose:%s, args:%s}" % \
                    (self.__opts.domain, self.__opts.range, self.brightness, self.transition_time,
                     self.delete, self.verbose, self.args)
