"""
Created on 4 Mar 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import socket

from scs_philips_hue.client.client_exception import ClientException
from scs_philips_hue.client.rest_client import RESTClient

from scs_philips_hue.data.bridge.response import Response

from scs_philips_hue.manager.bridge_manager import BridgeManager


# --------------------------------------------------------------------------------------------------------------------

class IPDiscovery(object):
    """
    classdocs
    """

    __BRIDGE_DEFAULT_TIMEOUT = 2            # seconds

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host, http_client):
        """
        Constructor
        """
        self.__host = host
        self.__http_client = http_client


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, credentials):
        # find...
        host = self.find_first()

        if host is None:
            return None

        # config...
        manager = BridgeManager(self.__http_client, host.ip_address, credentials.username)
        config = manager.find()

        # check...
        if config.bridge_id == credentials.bridge_id:
            return config

        return None


    def find_first(self):
        for ip_address in self.__host.scan(timeout=self.__BRIDGE_DEFAULT_TIMEOUT):
            if self.__is_bridge(ip_address):
                return IPHost(ip_address)

        return None


    def find_all(self):
        bridges = []

        for ip_address in self.__host.scan(timeout=self.__BRIDGE_DEFAULT_TIMEOUT):
            if self.__is_bridge(ip_address):
                bridges.append(IPHost(ip_address))

        return bridges


    # ----------------------------------------------------------------------------------------------------------------

    def __is_bridge(self, ip_address):
        rest_client = RESTClient(self.__http_client)

        try:
            # request...
            rest_client.connect(ip_address, None, timeout=self.__BRIDGE_DEFAULT_TIMEOUT)
            jdict = rest_client.get('/api')

            if jdict is None:
                return False

            # response...
            return Response.construct_from_jdict(jdict) is not None

        except (ClientException, OSError, socket.timeout):
            return False

        finally:
            rest_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "IPDiscovery:{host:%s, http_client:%s}" % (self.__host, self.__http_client)


# --------------------------------------------------------------------------------------------------------------------

class IPHost(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ip_address):
        """
        Constructor
        """
        self.__ip_address = ip_address


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def ip_address(self):
        return self.__ip_address


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "IPHost:{ip_address:%s}" % self.ip_address
