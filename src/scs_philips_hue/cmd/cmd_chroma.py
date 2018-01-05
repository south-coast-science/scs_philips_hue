"""
Created on 6 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_philips_hue.data.light.chroma import ChromaPoint


# --------------------------------------------------------------------------------------------------------------------

class CmdChroma(object):
    """unix command line handler"""

    __POINTS = {
        'R': ChromaPoint.red(),
        'G': ChromaPoint.green(),
        'B': ChromaPoint.blue(),
        'W': ChromaPoint.white_3000k()
    }


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog -d MIN MAX -r { R | G | B | W } { R | G | B | W }"
                                                    " [-t TRANSITION_TIME] [-b BRIGHTNESS] [-v]", version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--domain", "-d", type="float", nargs=2, action="store", dest="domain",
                                 help="domain minimum and maximum values (must be different values, min < max)")

        self.__parser.add_option("--range", "-r", type="string", nargs=2, action="store", dest="range",
                                 help="chromaticity of start and end points (must be different values)")

        # optional...
        self.__parser.add_option("--transition", "-t", type="float", nargs=1, action="store", dest="transition_time",
                                 default=1.0, help="transition time between settings (default 1.0 seconds)")

        self.__parser.add_option("--brightness", "-b", type="int", nargs=1, action="store", dest="brightness",
                                 default=254, help="brightness of light (1 to 254, default 254)")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__opts.domain is None or self.__opts.range is None:
            return False

        if self.domain_min >= self.domain_max:
            return False

        if self.range_min == self.range_max:
            return False

        if self.range_min not in self.__POINTS:
            return False

        if self.range_max not in self.__POINTS:
            return False

        if self.transition_time < 0.0:
            return False

        if self.brightness < 1 or self.brightness > 254:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def range_min_chroma(self):
        if self.range_min is None:
            return None

        return self.__POINTS[self.range_min]


    def range_max_chroma(self):
        if self.range_min is None:
            return None

        return self.__POINTS[self.range_max]


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def domain_min(self):
        if self.__opts.domain is None:
            return None

        return self.__opts.domain[0]


    @property
    def domain_max(self):
        if self.__opts.domain is None:
            return None

        return self.__opts.domain[1]


    @property
    def range_min(self):
        if self.__opts.range is None:
            return None

        return self.__opts.range[0]


    @property
    def range_max(self):
        if self.__opts.range is None:
            return None

        return self.__opts.range[1]


    @property
    def transition_time(self):
        return self.__opts.transition_time


    @property
    def brightness(self):
        return self.__opts.brightness


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
        return "CmdChroma:{domain:%s, range:%s, transition_time:%s, brightness:%s, verbose:%s, args:%s}" %  \
               (self.__opts.domain, self.__opts.range, self.transition_time, self.brightness, self.verbose, self.args)
