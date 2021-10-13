"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdLight(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { -a SERIAL_NUMBER | -s | -l | -d INDEX | -n INDEX NAME } "
                                                    "[-i INDENT] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--add", "-a", type="string", nargs=1, action="store", dest="add",
                                 help="add the light with SERIAL_NUMBER")

        self.__parser.add_option("--search", "-s", action="store_true", dest="search",
                                 help="search for new lights")

        self.__parser.add_option("--list", "-l", action="store_true", dest="list",
                                 help="list all lights")

        self.__parser.add_option("--delete", "-d", type="string", nargs=1, action="store", dest="delete",
                                 help="delete the light with INDEX")

        self.__parser.add_option("--name", "-n", type="string", nargs=2, action="store", dest="index_name",
                                 help="set the name of the light with INDEX to NAME")

        # output...
        self.__parser.add_option("--indent", "-i", type="int", nargs=1, action="store", dest="indent",
                                 help="pretty-print the output with INDENT")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        if self.add is not None:
            count += 1

        if self.search is not None:
            count += 1

        if self.list is not None:
            count += 1

        if self.delete is not None:
            count += 1

        if self.name is not None:
            count += 1

        if count != 1:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def add(self):
        return self.__opts.add


    @property
    def search(self):
        return self.__opts.search


    @property
    def list(self):
        return self.__opts.list


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def name(self):
        return self.__opts.index_name


    @property
    def indent(self):
        return self.__opts.indent


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdLight:{add:%s, search:%s, list:%s, delete:%s, name:%s, indent:%s, verbose:%s}" %  \
               (self.add, self.search, self.list, self.delete, self.name, self.indent, self.verbose)
