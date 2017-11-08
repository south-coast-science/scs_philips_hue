"""
Created on 30 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"light-id": "00:17:88:01:03:54:25:66-0b"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# TODO: use light group, not light

# --------------------------------------------------------------------------------------------------------------------

class Light(PersistentJSONable):
    """
    classdocs
    """

    __DIR =             "hue/"
    __FILENAME =        "light.json"

    @classmethod
    def filename(cls, host):
        return host.scs_dir() + cls.__DIR + cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return Light(None)

        light_id = jdict.get('light-id')

        return Light(light_id)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, light_id):
        """
        Constructor
        """
        super().__init__()

        self.__light_id = light_id                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['light-id'] = self.light_id

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def light_id(self):
        return self.__light_id


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Light:{light_id:%s, username:%s}" % self.light_id
