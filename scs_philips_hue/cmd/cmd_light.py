"""
Created on 4 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# TODO: migrate from run by index to run by name

# --------------------------------------------------------------------------------------------------------------------

class CmdLight(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-e] [-v] "
                                                    "{ -s | -l | -n INDEX NAME | -d INDEX | -r NAME_1..NAME_N }",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--search", "-s", action="store_true", dest="search",
                                 help="search for new lights")

        self.__parser.add_option("--list", "-l", action="store_true", dest="list",
                                 help="list all lights")

        self.__parser.add_option("--name", "-n", type="string", nargs=2, action="store", dest="index_name",
                                 help="set the name of the light with INDEX to NAME")

        self.__parser.add_option("--delete", "-d", type="string", nargs=1, action="store", dest="delete",
                                 help="delete the light with INDEX")

        self.__parser.add_option("--run", "-r", action="store_true", dest="run",
                                 help="direct stdin to the light(s) with INDEX_1..INDEX_N")

        self.__parser.add_option("--echo", "-e", action="store_true", dest="echo", default=False,
                                 help="echo stdin to stdout")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        if self.search is not None:
            count += 1

        if self.list is not None:
            count += 1

        if self.name is not None:
            count += 1

        if self.delete is not None:
            count += 1

        if self.run is not None:
            count += 1

        if count != 1:
            return False

        if self.run and self.args is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def search(self):
        return self.__opts.search


    @property
    def list(self):
        return self.__opts.list


    @property
    def name(self):
        return self.__opts.index_name


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def run(self):
        return self.__opts.run


    @property
    def run_indices(self):
        if not self.run:
            return None

        return self.__args


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
        return "CmdLight:{search:%s, list:%s, name:%s, delete:%s, run:%s, echo:%s, verbose:%s, args:%s}" %  \
               (self.search, self.list, self.name, self.delete, self.run, self.echo, self.verbose, self.args)
