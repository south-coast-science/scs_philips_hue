"""
Created on 23 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdMQTTSubscriber(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog {-c | -t TOPIC_PATH } [-v]", version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--conf", "-c", action="store_true", dest="use_domain_conf", default=False,
                                 help="get topic path from domain conf")

        self.__parser.add_option("--topic", "-t", type="string", nargs=1, action="store", dest="topic_path",
                                 help="use the given topic path")

        # optional...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()

    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.use_domain_conf and self.topic_path is not None:
            return False

        if not self.use_domain_conf and self.topic_path is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def use_domain_conf(self):
        return self.__opts.use_domain_conf


    @property
    def topic_path(self):
        return self.__opts.topic_path


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
        return "CmdMQTTSubscriber:{use_domain_conf:%s, topic_path:%s, verbose:%s, args:%s}" % \
               (self.use_domain_conf, self.topic_path, self.verbose, self.args)
