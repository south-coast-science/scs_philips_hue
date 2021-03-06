"""
Created on 4 Mar 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

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
        self.__host = host


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, credentials, timeout=None):
        timeout_time = None if timeout is None else time.time() + timeout

        while True:
            # UPnP...
            upnp = UPnPDiscovery()
            bridge = upnp.find(credentials.bridge_id)

            if bridge:
                return bridge

            # IP scan...
            scanner = IPDiscovery(self.__host)
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
            upnp = UPnPDiscovery()
            bridges = upnp.find_all()

            if bridges:
                return bridges

            # IP scan...
            scanner = IPDiscovery(self.__host)
            bridge = scanner.find_first()

            if bridge:
                return [bridge]

            if timeout_time and time.time() > timeout_time:
                return []

            time.sleep(self.__RETRY_DELAY)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Discovery:{host:%s}" % self.__host
