"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{
    "hue-br1-001": {
        "bridge-id": "001788FFFEAF8430",
        "username": "DN5YzKBncC6n69gjlKZqa6SRqZofXTmhZkrdnqG2"
    },
    "hue-br1-002": {
        "bridge-id": "001788FFFE795620",
        "username": "suLJJv6OgxG0UjwB9Uz7e1j08Xj36MOfFdxNNUmR"
    }
}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable, PersistentJSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class BridgeCredentials(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, name, jdict):
        if not jdict:
            return None

        bridge_id = jdict.get('bridge-id')
        username = jdict.get('username')

        return cls(name, bridge_id, username)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, bridge_id, username):
        """
        Constructor
        """
        super().__init__()

        self.__name = name                              # string
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
    def name(self):
        return self.__name


    @property
    def bridge_id(self):
        return self.__bridge_id


    @property
    def username(self):
        return self.__username


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BridgeCredentials:{name:%s, bridge_id:%s, username:%s}" % \
            (self.name, self.bridge_id, self.username)


# --------------------------------------------------------------------------------------------------------------------

class BridgeCredentialsSet(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "bridge_credentials_set.json"

    @classmethod
    def persistence_location(cls):
        return cls.hue_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(OrderedDict()) if skeleton else None

        credentials = OrderedDict()
        for name, credentials_jdict in jdict.items():
            credentials[name] = BridgeCredentials.construct_from_jdict(name, credentials_jdict)

        return cls(credentials)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, credentials):
        """
        Constructor
        """
        super().__init__()

        self.__credentials = credentials                 # dict of name: BridgeCredentials


    # ----------------------------------------------------------------------------------------------------------------

    def add(self, credentials: BridgeCredentials):
        self.__credentials[credentials.name] = credentials


    def delete(self, name):
        try:
            del self.__credentials[name]
            return True

        except KeyError:
            return False


    def credentials(self, name):
        return self.__credentials[name]                          # may raise KeyError


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.sorted_credentials


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sorted_credentials(self):
        return OrderedDict(sorted(self.__credentials.items()))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BridgeCredentialsSet:{credentials:%s}" % Str.collection(self.sorted_credentials)
