"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_philips_hue.data.bridge.bridge_config import ReportedBridgeConfig

from scs_philips_hue.manager.manager import Manager


# --------------------------------------------------------------------------------------------------------------------

class UserManager(Manager):
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

    def find(self, username):
        entries = self.find_all()

        for entry in entries:
            if entry.username == username:
                return entry

        return None


    def find_all(self):
        request_path = '/config'

        # request...
        self._rest_client.connect(self._host, self._username)

        try:
            jdict = self._rest_client.get(request_path)
        finally:
            self._rest_client.close()

        # response...
        config = ReportedBridgeConfig.construct_from_jdict(jdict)
        whitelist = config.whitelist

        return whitelist.entries


    # ----------------------------------------------------------------------------------------------------------------

    # def update(self, user_id, user):
    #     request_path = '/v1/users/' + user_id
    #
        # request...
        # self.__rest_client.connect()
        #
        # try:
        #     self.__rest_client.put(request_path, user.as_json())
        # finally:
        #     self.__rest_client.close()
