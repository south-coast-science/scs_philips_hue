"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"path-name": "risk", "domain-min": 5, "domain-max": 30, "brightness": 254, "transition-time": 9}
"""

import os

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable

from scs_philips_hue.config.chroma_path import ChromaPath
from scs_philips_hue.data.light.chroma import ChromaMapping


# --------------------------------------------------------------------------------------------------------------------

class ChromaConf(PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __DIR =             "hue"
    __FILENAME =        "chroma_conf.json"

    @classmethod
    def persistence_location(cls, host):
        return os.path.join(host.scs_dir(), cls.__DIR), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        path_name = jdict.get('path-name')

        domain_min = jdict.get('domain-min')
        domain_max = jdict.get('domain-max')

        brightness = jdict.get('brightness')
        transition_time = jdict.get('transition-time')

        return cls(path_name, domain_min, domain_max, brightness, transition_time)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path_name, domain_min, domain_max, brightness, transition_time):
        """
        Constructor
        """
        super().__init__()

        self.__path_name = path_name                                # string

        self.__domain_min = domain_min                              # float
        self.__domain_max = domain_max                              # float

        self.__brightness = Datum.int(brightness)                   # int
        self.__transition_time = Datum.int(transition_time)         # int


    # ----------------------------------------------------------------------------------------------------------------

    def path(self):
        return ChromaPath.load_default(self.path_name)


    def mapping(self, path):
        return ChromaMapping.construct(self, path)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['path-name'] = self.path_name

        jdict['domain-min'] = self.domain_min
        jdict['domain-max'] = self.domain_max

        jdict['brightness'] = self.brightness
        jdict['transition-time'] = self.transition_time

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path_name(self):
        return self.__path_name


    @property
    def domain_min(self):
        return self.__domain_min


    @property
    def domain_max(self):
        return self.__domain_max


    @property
    def brightness(self):
        return self.__brightness


    @property
    def transition_time(self):
        return self.__transition_time


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ChromaConf:{path_name:%s, domain_min:%s, domain_max:%s, brightness:%s, transition_time:%s}" % \
               (self.path_name, self.domain_min, self.domain_max, self.brightness, self.transition_time)
