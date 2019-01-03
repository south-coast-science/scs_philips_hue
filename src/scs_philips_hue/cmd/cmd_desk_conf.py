"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"lamp-names": ["scs-hcl-001", "scs-hcl-002"]}
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdDeskConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ -a LAMP_NAME | -r LAMP_NAME | -x }] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--add", "-a", type="string", nargs=1, action="store", dest="add_lamp",
                                 help="add the given lamp")

        self.__parser.add_option("--remove", "-r", type="string", nargs=1, action="store", dest="remove_lamp",
                                 help="remove the given lamp")

        self.__parser.add_option("--delete", "-x", action="store_true", dest="delete",
                                 help="delete the desk configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.add_lamp is not None and self.remove_lamp is not None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def add_lamp(self):
        return self.__opts.add_lamp


    @property
    def remove_lamp(self):
        return self.__opts.remove_lamp


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdDeskConf:{add_lamp:%s, remove_lamp:%s, delete:%s, verbose:%s}" % \
                    (self.add_lamp, self.remove_lamp, self.delete, self.verbose)
