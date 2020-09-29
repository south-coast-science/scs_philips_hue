"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_philips_hue.data.bridge.bridge_config import ReportedBridgeConfig
from scs_philips_hue.data.bridge.response import Response

from scs_philips_hue.manager.manager import Manager


# --------------------------------------------------------------------------------------------------------------------

class BridgeManager(Manager):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host, username):
        """
        Constructor
        """
        super().__init__(host, username)


    # ----------------------------------------------------------------------------------------------------------------

    def find(self):
        request_path = '/config'

        # request...
        self._rest_client.connect(self._host, self._username)

        try:
            jdict = self._rest_client.get(request_path)
        finally:
            self._rest_client.close()

        # response...
        config = ReportedBridgeConfig.construct_from_jdict(jdict)

        return config


    def set_config(self, config):
        request_path = '/config'

        # request...
        self._rest_client.connect(self._host, self._username)

        try:
            jdict = self._rest_client.put(request_path, config.as_json())
        finally:
            self._rest_client.close()

        # response...
        response = Response.construct_from_jdict(jdict)

        return response


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
