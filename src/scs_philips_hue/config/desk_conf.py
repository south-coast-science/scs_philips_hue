"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Lamp names form an ordered set. The most-recently added lamp is at the end of the list.

document example:
{"lamp-names": ["scs-hcl-001", "scs-hcl-002"]}
"""

from collections import OrderedDict

from scs_core.data.json import MultiPersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class DeskConf(MultiPersistentJSONable):
    """
    classdocs
    """

    __FILENAME =        "desk_conf.json"

    @classmethod
    def persistence_location(cls, name):
        filename = cls.__FILENAME if name is None else '_'.join((name, cls.__FILENAME))

        return cls.hue_dir(), filename


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, name=None, default=True):
        if not jdict:
            return None

        lamp_names = jdict.get('lamp-names')

        return cls(lamp_names, name=name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, lamp_names, name=None):
        """
        Constructor
        """
        super().__init__(name)

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
        return "DeskConf:{name:%s, lamp_names:%s}" % (self.name, self.lamp_names)
