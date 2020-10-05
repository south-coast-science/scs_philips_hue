"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Lamp names form an ordered set. The most-recently added lamp is at the end of the list.

document example:
{"lamp-names": ["scs-hcl-001", "scs-hcl-002"]}
"""

import os

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class DeskConf(PersistentJSONable):
    """
    classdocs
    """

    __DIR =             "hue"
    __FILENAME =        "desk_conf.json"

    @classmethod
    def persistence_location(cls, host):
        return os.path.join(host.scs_dir(), cls.__DIR), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        lamp_names = jdict.get('lamp-names')

        return cls(lamp_names)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, lamp_names):
        """
        Constructor
        """
        super().__init__()

        self.__lamp_names = lamp_names                  # list of string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['lamp-names'] = self.lamp_names

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def add_lamp(self, lamp_name):
        if lamp_name in self.__lamp_names:
            return

        self.__lamp_names.append(lamp_name)


    def remove_lamp(self, lamp_name):
        if lamp_name not in self.__lamp_names:
            return

        self.__lamp_names.remove(lamp_name)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def lamp_names(self):
        return self.__lamp_names


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeskConf:{lamp_names:%s}" % self.lamp_names
