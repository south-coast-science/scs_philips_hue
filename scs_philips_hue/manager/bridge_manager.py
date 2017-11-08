"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_philips_hue.data.bridge.bridge_config import BridgeConfig
from scs_philips_hue.data.bridge.response import Response

from scs_philips_hue.manager.manager import Manager


# --------------------------------------------------------------------------------------------------------------------

class BridgeManager(Manager):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, host, username):
        """
        Constructor
        """
        super().__init__(http_client, host, username)


    # ----------------------------------------------------------------------------------------------------------------

    def find_config(self):
        request_path = '/config'

        # request...
        self._rest_client.connect(self._host, self._username)

        try:
            jdict = self._rest_client.get(request_path)
        finally:
            self._rest_client.close()

        # response...
        config = BridgeConfig.construct_from_jdict(jdict)

        return config


    # ----------------------------------------------------------------------------------------------------------------

    def register(self, device):
        # request...
        self._rest_client.connect(self._host, None)

        try:
            jdict = self._rest_client.post('', device.as_json())
        finally:
            self._rest_client.close()

        # response...
        response = Response.construct_from_jdict(jdict)

        return response
