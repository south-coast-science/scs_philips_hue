"""
Created on 30 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_philips_hue.data.bridge.bridge_summary import BridgeSummary

from scs_philips_hue.client.upnp_client import UPnPClient


# --------------------------------------------------------------------------------------------------------------------

class UPnPDiscovery(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        """
        Constructor
        """
        self.__upnp_client = UPnPClient(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, id):
        descriptions = self.find_all()

        for description in descriptions:
            if description.id == id:
                return description

        return None


    def find_all(self):
        # request...
        try:
            self.__upnp_client.connect()
            response_jdict = self.__upnp_client.get()
        finally:
            self.__upnp_client.close()

        # response...
        descriptions = [BridgeSummary.construct_from_jdict(jdict) for jdict in response_jdict]

        return descriptions


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UPnPDiscovery:{upnp_client:%s}" % self.__upnp_client
