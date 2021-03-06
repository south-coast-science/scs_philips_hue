"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"path-name": "risk", "domain-min": 5, "domain-max": 30, "brightness": 254, "transition-time": 9}
"""

import optparse

from scs_philips_hue.config.chroma_path import ChromaPath


# --------------------------------------------------------------------------------------------------------------------

class CmdChromaConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        path_names = ' | '.join(ChromaPath.defaults())

        self.__parser = optparse.OptionParser(usage="%prog [-p PATH_NAME] [-l DOMAIN_MIN] [-u DOMAIN_MAX] "
                                                    "[-b BRIGHTNESS] [-t TRANSITION] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--path", "-p", type="string", nargs=1, action="store", dest="path_name",
                                 help="name of chroma path { %s }" % path_names)

        self.__parser.add_option("--lower", "-l", type="float", nargs=1, action="store", dest="domain_min",
                                 help="specify the domain lower bound")

        self.__parser.add_option("--upper", "-u", type="float", nargs=1, action="store", dest="domain_max",
                                 help="specify the domain upper bound")

        self.__parser.add_option("--bright", "-b", type="int", nargs=1, action="store", dest="brightness",
                                 help="set the lamp brightness (max 254)")

        self.__parser.add_option("--trans", "-t", type="float", nargs=1, action="store", dest="transition_time",
                                 help="set the lamp transition time (seconds)")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.path_name is not None and self.path_name not in ChromaPath.defaults():
            return False

        if self.brightness is not None and (self.brightness < 0 or self.brightness > 254):
            return False

        return True


    def is_complete(self):
        if self.path_name is None or self.domain_min is None or self.domain_max is None or \
                self.brightness is None or self.transition_time is None:
            return False

        return True


    def set(self):
        return self.path_name is not None or self.domain_min is not None or self.domain_max is not None or \
               self.brightness is not None or self.transition_time is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path_name(self):
        return self.__opts.path_name


    @property
    def domain_min(self):
        return self.__opts.domain_min


    @property
    def domain_max(self):
        return self.__opts.domain_max


    @property
    def brightness(self):
        return self.__opts.brightness


    @property
    def transition_time(self):
        return self.__opts.transition_time


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdChromaConf:{path_name:%s, domain_min:%s, domain_max:%s, " \
               "brightness:%s, transition_time:%s, verbose:%s}" % \
                    (self.path_name, self.domain_min, self.domain_max,
                     self.brightness, self.transition_time, self.verbose)
