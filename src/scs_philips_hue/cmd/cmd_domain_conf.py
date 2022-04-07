"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"topic-path": "/orgs/south-coast-science-demo/brighton/loc/1/particulates", "document-node": "val.pm10"}
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdDomainConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-n NAME { -a TOPIC_PATH DOMAIN_NODE | -r }] "
                                                    "[-i INDENT] [-v]", version="%prog 1.0")

        # configuration...
        self.__parser.add_option("--name", "-n", type="string", nargs=1, action="store", dest="name",
                                 help="the name of the desk configuration")

        # functions...
        self.__parser.add_option("--add", "-a", type="string", nargs=2, action="store", dest="add",
                                 help="add the domain configuration")

        self.__parser.add_option("--remove", "-r", action="store_true", dest="remove", default=False,
                                 help="remove the domain configuration")

        # output...
        self.__parser.add_option("--indent", "-i", type="int", nargs=1, action="store", dest="indent",
                                 help="pretty-print the output with INDENT")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.add is not None and self.remove:
            return False

        if (self.add is not None or self.remove) and self.name is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__opts.name


    @property
    def add(self):
        return self.__opts.add


    @property
    def remove(self):
        return self.__opts.remove


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
        return "CmdDomainConf:{name:%s, add:%s, remove:%s, indent:%s, verbose:%s}" % \
                    (self.name, self.add, self.remove, self.indent, self.verbose)
