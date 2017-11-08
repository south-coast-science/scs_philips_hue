"""
Created on 6 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_philips_hue.data.light.chroma import ChromaPoint


# TODO: replace z / u with gamut - two params

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
        self.__parser = optparse.OptionParser(usage="%prog -m MAX_VALUE -z { R | G | B | W } -u { R | G | B | W }"
                                                    " [-t TIME] [-b BRIGHTNESS] [-v]", version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--max-value", "-m", type="float", nargs=1, action="store", dest="max_value",
                                 help="maximum input value")

        self.__parser.add_option("--zero-point", "-z", type="string", nargs=1, action="store", dest="zero_point",
                                 help="chromaticity for zero input value and below")

        self.__parser.add_option("--upper-point", "-u", type="string", nargs=1, action="store", dest="upper_point",
                                 help="chromaticity for maximum input value and above "
                                      "(must be different from zero point)")

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
        if self.max_value is None or self.zero_point is None or self.upper_point is None:
            return False

        if self.zero_point not in self.__POINTS:
            return False

        if self.upper_point not in self.__POINTS:
            return False

        if self.zero_point == self.upper_point:
            return False

        if self.transition_time < 0.0:
            return False

        if self.brightness < 1 or self.brightness > 254:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def zero_chroma(self):
        return self.__POINTS[self.zero_point]


    def upper_chroma(self):
        return self.__POINTS[self.upper_point]


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def max_value(self):
        return self.__opts.max_value


    @property
    def zero_point(self):
        return self.__opts.zero_point


    @property
    def upper_point(self):
        return self.__opts.upper_point


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
        return "CmdChroma:{max_value:%s, zero_point:%s, upper_point:%s, transition_time:%s, brightness:%s, " \
               "verbose:%s, args:%s}" %  \
               (self.max_value, self.zero_point, self.upper_point, self.transition_time, self.brightness,
                self.verbose, self.args)
