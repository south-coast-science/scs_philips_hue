"""
Created on 19 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_core.data.datum import Datum

from scs_philips_hue.data.bridge.bridge_config import BridgeConfig


# --------------------------------------------------------------------------------------------------------------------

class CmdBridge(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-n NAME] [-p PORTAL_SERVICES] [-c CHECK_UPDATE] "
                                                    "[-u DO_UPDATE] [-z CHANNEL] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--name", "-n", type="string", nargs=1, action="store", dest="name",
                                 help="set the name of the bridge to NAME (between 4 and 16 chars)")

        self.__parser.add_option("--portal", "-p", type="int", nargs=1, action="store", dest="portal_services",
                                 help="enable portal services (1 or 0)")

        self.__parser.add_option("--check", "-c", type="int", nargs=1, action="store", dest="check_update",
                                 help="check for software update (1 or 0)")

        self.__parser.add_option("--update", "-u", type="int", nargs=1, action="store", dest="do_update",
                                 help="perform software update, if available (1 or 0)")

        self.__parser.add_option("--zigbee", "-z", type="string", nargs=1, action="store", dest="zigbee_channel",
                                 help="set zigbee channel (11, 15, 20 or 25)")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.name is not None:
            if len(self.name) < BridgeConfig.NAME_MIN_LENGTH or len(self.name) > BridgeConfig.NAME_MAX_LENGTH:
                return False

        if self.__opts.check_update is not None:
            if self.__opts.check_update != 0 and self.__opts.check_update != 1:
                return False

        if self.__opts.do_update is not None:
            if self.__opts.do_update != 0 and self.__opts.do_update != 1:
                return False

        if self.zigbee_channel is not None:
            if self.__opts.zigbee not in BridgeConfig.ZIGBEE_CHANNELS:
                return False

        return True


    def set(self):
        return self.name is not None or self.__opts.update is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__opts.name


    @property
    def portal_services(self):
        return Datum.bool(self.__opts.portal_services)


    @property
    def check_update(self):
        return Datum.bool(self.__opts.check_update)


    @property
    def do_update(self):
        return Datum.bool(self.__opts.do_update)


    @property
    def zigbee_channel(self):
        return self.__opts.zigbee_channel


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdBridge:{name:%s, portal_services:%s, check_update:%s, do_update:%s, zigbee_channel:%s, " \
               "verbose:%s}" %  \
               (self.name, self.portal_services, self.check_update, self.do_update, self.zigbee_channel,
                self.verbose)
