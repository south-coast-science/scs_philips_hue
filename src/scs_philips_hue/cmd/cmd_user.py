"""
Created on 3 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdUser(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog {-d USER | -l }  [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--delete", "-d", type="string", nargs=1, action="store", dest="delete",
                                 help="delete user")

        self.__parser.add_option("--list", "-l", action="store_true", dest="list",
                                 help="list all users")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.delete is None and not self.list:
            return False

        if self.delete is not None and self.list:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def delete(self):
        return self.__opts.delete


    @property
    def list(self):
        return self.__opts.list


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
        return "CmdUser:{delete:%s, list:%s, verbose:%s, args:%s}" %  \
               (self.delete, self.list, self.verbose, self.args)
