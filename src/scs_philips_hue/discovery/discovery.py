"""
Created on 4 Mar 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sys.logging import Logging

from scs_philips_hue.discovery.ip_discovery import IPDiscovery
from scs_philips_hue.discovery.upnp_discovery import UPnPDiscovery


# --------------------------------------------------------------------------------------------------------------------

class Discovery(object):
    """
    classdocs
    """

    __RETRY_DELAY = 10.0                # seconds

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host):
        """
        Constructor
        """
        self.__host = host                                          # PersistenceManager
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, credentials):
        # UPnP...
        self.__logger.info("find by UPnP...")
        upnp = UPnPDiscovery()
        bridge = upnp.find(credentials.bridge_id)

        if bridge:
            return bridge

        # IP scan...
        self.__logger.info("find by IP scan...")
        scanner = IPDiscovery(self.__host)

        return scanner.find(credentials)


    def find_all(self):
        # UPnP...
        self.__logger.info("find by UPnP...")
        upnp = UPnPDiscovery()
        bridges = upnp.find_all()

        if bridges:
            return bridges

        # IP scan...
        self.__logger.info("find by IP scan...")
        scanner = IPDiscovery(self.__host)

        return scanner.find_all()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Discovery:{host:%s}" % self.__host
