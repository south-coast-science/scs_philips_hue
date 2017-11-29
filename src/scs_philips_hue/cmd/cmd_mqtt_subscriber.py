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
        self.__parser = optparse.OptionParser(usage="%prog "
                                                    "[-s] [SUB_TOPIC_1 (UDS_SUB_1) .. SUB_TOPIC_N (UDS_SUB_N)] "
                                                    "[-e] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--sub", "-s", action="store_true", dest="uds_sub",
                                 help="write subscriptions to UDS instead of stdout")

        self.__parser.add_option("--echo", "-e", action="store_true", dest="echo", default=False,
                                 help="echo input to stdout (if writing subscriptions to DomainSocket)")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.echo and not self.__opts.uds_sub:
            return False

        if self.__opts.uds_sub and len(self.__args) % 2 != 0:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def subscriptions(self):
        subscriptions = []

        if self.__opts.uds_sub:
            for i in range(0, len(self.__args), 2):
                subscriptions.append(Subscription(self.__args[i], self.__args[i + 1]))
        else:
            for i in range(len(self.__args)):
                subscriptions.append(Subscription(self.__args[i]))

        return subscriptions


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
        subscriptions = '[' + ', '.join(str(subscription) for subscription in self.subscriptions) + ']'

        return "CmdMQTTSubscriber:{subscriptions:%s, echo:%s, verbose:%s, args:%s}" % \
               (subscriptions, self.echo, self.verbose, self.args)


# --------------------------------------------------------------------------------------------------------------------

class Subscription(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, address=None):
        """
        Constructor
        """
        self.__topic = topic            # string        topic path
        self.__address = address        # string        DomainSocket address


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def address(self):
        return self.__address


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Subscription:{topic:%s, address:%s}" % (self.topic, self.address)
