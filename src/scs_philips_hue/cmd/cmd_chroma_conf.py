"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"domain-min": 0.0, "domain-max": 50.0, "range-min": [0.08, 0.84], "range-max": [0.74, 0.26],
"brightness": 128, "transition-time": 9}
"""

import optparse

from scs_philips_hue.config.chroma_conf import ChromaMin, ChromaInterval
from scs_philips_hue.data.light.chroma import ChromaPoint


# --------------------------------------------------------------------------------------------------------------------

class CmdChromaConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-m DOMAIN_MIN CHR_X CHR_Y] "
                                                    "[-i DOMAIN_MAX CHR_X CHR_Y] [-d DOMAIN_MAX] "
                                                    "[-b BRIGHTNESS] [-t TRANSITION] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--min", "-m", type="float", nargs=3, action="store", dest="minimum",
                                 help="set minimum values")

        self.__parser.add_option("--int", "-i", type="float", nargs=3, action="store", dest="insert_interval",
                                 help="add or update an interval with the given DOMAIN_MAX")

        self.__parser.add_option("--del", "-d", type="float", nargs=1, action="store", dest="delete_interval",
                                 help="delete the interval with the given DOMAIN_MAX")

        self.__parser.add_option("--bright", "-b", type="int", nargs=1, action="store", dest="brightness",
                                 help="set the lamp brightness (max 254)")

        self.__parser.add_option("--trans", "-t", type="float", nargs=1, action="store", dest="transition_time",
                                 help="set the lamp transition time (seconds)")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.brightness is not None and (self.brightness < 0 or self.brightness > 254):
            return False

        return True


    def is_complete(self):
        if self.minimum is None or self.insert_interval is None or \
                self.brightness is None or self.transition_time is None:
            return False

        return True


    def set(self):
        return self.minimum is not None or self.insert_interval is not None or \
               self.brightness is not None or self.transition_time is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def minimum(self):
        if self.__opts.minimum is None:
            return None

        return ChromaMin(self.__opts.minimum[0], ChromaPoint(self.__opts.minimum[1], self.__opts.minimum[2]))


    @property
    def insert_interval(self):
        if self.__opts.insert_interval is None:
            return None

        point = ChromaPoint(self.__opts.insert_interval[1], self.__opts.insert_interval[2])

        return ChromaInterval(self.__opts.insert_interval[0], point)


    @property
    def delete_interval(self):
        return self.__opts.delete_interval


    @property
    def brightness(self):
        return self.__opts.brightness


    @property
    def transition_time(self):
        return self.__opts.transition_time


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
        return "CmdChromaConf:{minimum:%s, insert_interval:%s, delete_interval:%s, " \
               "brightness:%s, transition_time:%s, verbose:%s, args:%s}" % \
                    (self.minimum, self.insert_interval, self.delete_interval,
                     self.brightness, self.transition_time, self.verbose, self.args)
