"""
Created on 7 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"lastscan": "2017-11-07T12:10:47", "1": {"name": "Hue color lamp 1"}}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class LightName(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        name = jdict.get('name')

        return LightName(name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name):
        """
        Constructor
        """
        self.__name = name                          # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['name'] = self.name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LightName:{name:%s}" % self.name


# --------------------------------------------------------------------------------------------------------------------

class LightScanEntry(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, index, jdict):
        if not jdict:
            return None

        name = LightName.construct_from_jdict(jdict)

        return LightScanEntry(index, name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, index, name):
        """
        Constructor
        """
        self.__index = index                            # index
        self.__name = name                              # LightName


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict[self.index] = self.name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def index(self):
        return self.__index


    @property
    def name(self):
        return self.__name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LightScanEntry:{index:%s, name:%s}" %  (self.index, self.name)
