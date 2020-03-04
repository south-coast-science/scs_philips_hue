"""
Created on 4 Mar 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_philips_hue.discovery.ip_discovery import IPDiscovery
from scs_philips_hue.discovery.upnp_discovery import UPnPDiscovery


# --------------------------------------------------------------------------------------------------------------------

class Discovery(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host, http_client):
        """
        Constructor
        """
        self.__host = host
        self.__http_client = http_client


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, credentials):
        # UPnP...
        upnp = UPnPDiscovery(self.__http_client)
        bridge = upnp.find(credentials.bridge_id)

        if bridge:
            return bridge

        # IP scan...
        scanner = IPDiscovery(self.__host, self.__http_client)
        bridge = scanner.find(credentials)

        return bridge


    def find_all(self):
        # UPnP...
        upnp = UPnPDiscovery(self.__http_client)
        bridges = upnp.find_all()

        if bridges:
            return bridges

        # IP scan...
        scanner = IPDiscovery(self.__host, self.__http_client)
        bridge = scanner.find_first()

        if bridge:
            return [bridge]

        return []


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Discovery:{host:%s, http_client:%s}" % (self.__host, self.__http_client)
