"""
Created on 26 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"ipv4": "192.168.2.29"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable
from scs_core.sys.ipv4_address import IPv4Address


# --------------------------------------------------------------------------------------------------------------------

class BridgeAddress(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "bridge_address.json"

    @classmethod
    def persistence_location(cls):
        return cls.hue_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(None) if skeleton else None

        ipv4 = IPv4Address.construct(jdict.get('ipv4'))

        return cls(ipv4)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ipv4):
        """
        Constructor
        """
        super().__init__()

        self.__ipv4 = ipv4                                  # IPv4Address


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['ipv4'] = None if self.ipv4 is None else self.ipv4.dot_decimal()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def ipv4(self):
        return self.__ipv4


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BridgeAddress:{ipv4:%s}" % self.ipv4
