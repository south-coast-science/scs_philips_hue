"""
Created on 4 Mar 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_philips_hue.discovery.ip_discovery import IPDiscovery
from scs_philips_hue.discovery.upnp_discovery import UPnPDiscovery


# TODO: can we report connected bridges that we are not users of?

# --------------------------------------------------------------------------------------------------------------------

class Discovery(object):
    """
    classdocs
    """

    __RETRY_DELAY = 10.0                # seconds

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host, http_client):
        """
        Constructor
        """
        self.__host = host
        self.__http_client = http_client


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, credentials, timeout=None):
        timeout_time = None if timeout is None else time.time() + timeout

        while True:
            # UPnP...
            upnp = UPnPDiscovery(self.__http_client)
            bridge = upnp.find(credentials.bridge_id)

            if bridge:
                return bridge

            # IP scan...
            scanner = IPDiscovery(self.__host, self.__http_client)
            bridge = scanner.find(credentials)

            if bridge:
                return bridge

            if timeout_time and time.time() > timeout_time:
                return None

            time.sleep(self.__RETRY_DELAY)


    def find_all(self, timeout=None):
        timeout_time = None if timeout is None else time.time() + timeout

        while True:
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

            if timeout_time and time.time() > timeout_time:
                return []

            time.sleep(self.__RETRY_DELAY)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Discovery:{host:%s, http_client:%s}" % (self.__host, self.__http_client)
