"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdDesk(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-e] [-v] NAME_1..NAME_N }", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--echo", "-e", action="store_true", dest="echo", default=False,
                                 help="echo stdin to stdout")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.args is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def echo(self):
        return self.__opts.echo


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
        return "CmdDesk:{echo:%s, verbose:%s, args:%s}" %   (self.echo, self.verbose, self.args)
