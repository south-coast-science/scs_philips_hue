"""
Created on 26 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

example document:
{"org-id": "south-coast-science-test-user", "api-key": "9fdfb841-3433-45b8-b223-3f5a283ceb8e"}
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdBridgeAddress(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{-s DOT_DECIMAL | -d }] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--set", "-s", type="string", nargs=1, action="store", dest="set_dot_decimal",
                                 help="set IPv4 address")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set_dot_decimal and self.delete:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def set_dot_decimal(self):
        return self.__opts.set_dot_decimal


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def delete(self):
        return self.__opts.delete


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdBridgeAddress:{set_dot_decimal:%s, delete:%s, verbose:%s}" % \
               (self.set_dot_decimal, self.delete, self.verbose)
