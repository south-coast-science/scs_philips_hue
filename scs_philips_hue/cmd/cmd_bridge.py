"""
Created on 19 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdBridge(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-n NAME] [-u UPDATE] [-z CHANNEL] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--name", "-n", type="string", nargs=1, action="store", dest="name",
                                 help="set the name of the bridge to NAME (between 4 and 16 chars)")

        self.__parser.add_option("--update", "-u", type="int", nargs=1, action="store", dest="update",
                                 help="check for software update (1 or 0)")

        self.__parser.add_option("--zigbee", "-z", type="string", nargs=1, action="store", dest="zigbee",
                                 help="set zigbee channel (11, 15, 20 or 25)")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.name is not None:
            if len(self.name) < 4 or len(self.name) > 16:
                return False

        if self.__opts.update is not None:
            if self.__opts.update != 0 and self.__opts.update != 1:
                return False

        if self.zigbee is not None:
            if self.__opts.zigbee not in ["11", "15", "20" or "25"]:
                return False

        return True


    def set(self):
        return self.name is not None or self.__opts.update is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__opts.name


    @property
    def update(self):
        if self.__opts.update is None:
            return None

        return bool(self.__opts.update)


    @property
    def zigbee(self):
        return self.__opts.zigbee


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
        return "CmdBridge:{name:%s, update:%s, zigbee:%s, verbose:%s, args:%s}" %  \
               (self.name, self.update, self.zigbee, self.verbose, self.args)
