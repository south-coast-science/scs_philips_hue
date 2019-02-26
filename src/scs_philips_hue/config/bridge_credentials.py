"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"bridge-id": "001788fffe795620", "username": "b8bvymOH-ceugK8gBOpjeNeL0OMhXOEBQZosfsTx"}
"""

import os

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class BridgeCredentials(PersistentJSONable):
    """
    classdocs
    """

    __DIR =             "hue"
    __FILENAME =        "bridge_credentials.json"

    @classmethod
    def persistence_location(cls, host):
        return os.path.join(host.scs_dir(), cls.__DIR), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return BridgeCredentials(None, None)

        bridge_id = jdict.get('bridge-id')
        username = jdict.get('username')

        return BridgeCredentials(bridge_id, username)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, bridge_id, username):
        """
        Constructor
        """
        super().__init__()

        self.__bridge_id = bridge_id                    # string
        self.__username = username                      # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['bridge-id'] = self.bridge_id
        jdict['username'] = self.username

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def bridge_id(self):
        return self.__bridge_id


    @property
    def username(self):
        return self.__username


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BridgeCredentials:{bridge_id:%s, username:%s}" % (self.bridge_id, self.username)
