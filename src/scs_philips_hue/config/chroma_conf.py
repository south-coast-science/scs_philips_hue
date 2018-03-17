"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"domain-min": 0.0, "domain-max": 50.0, "range-min": [0.08, 0.84], "range-max": [0.74, 0.26],
"brightness": 128, "transition-time": 9}
"""

import os

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import PersistentJSONable

from scs_philips_hue.data.light.chroma import ChromaPoint


# --------------------------------------------------------------------------------------------------------------------

class ChromaConf(PersistentJSONable):
    """
    classdocs
    """

    CANONICAL_CHROMAS = {
        'R': ChromaPoint.red(),
        'G': ChromaPoint.green(),
        'B': ChromaPoint.blue(),
        'W': ChromaPoint.white_3000k()
    }


    # ----------------------------------------------------------------------------------------------------------------

    __DIR =             "hue"
    __FILENAME =        "chroma_conf.json"

    @classmethod
    def filename(cls, host):
        return os.path.join(host.scs_dir(), cls.__DIR, cls.__FILENAME)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        domain_min = jdict.get('domain-min')
        domain_max = jdict.get('domain-max')

        range_min = ChromaPoint.construct_from_jdict(jdict.get('range-min'))
        range_max = ChromaPoint.construct_from_jdict(jdict.get('range-max'))

        brightness = jdict.get('brightness')
        transition_time = jdict.get('transition-time')

        return ChromaConf(domain_min, domain_max, range_min, range_max, brightness, transition_time)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, domain_min, domain_max, range_min, range_max, brightness, transition_time):
        """
        Constructor
        """
        super().__init__()

        self.__domain_min = Datum.float(domain_min, 1)          # float
        self.__domain_max = Datum.float(domain_max, 1)          # float

        self.__range_min = range_min                            # ChromaPoint
        self.__range_max = range_max                            # ChromaPoint

        self.__brightness = Datum.int(brightness)               # int
        self.__transition_time = Datum.int(transition_time)     # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['domain-min'] = self.domain_min
        jdict['domain-max'] = self.domain_max

        jdict['range-min'] = self.range_min
        jdict['range-max'] = self.range_max

        jdict['brightness'] = self.brightness
        jdict['transition-time'] = self.transition_time

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def domain_min(self):
        return self.__domain_min


    @property
    def domain_max(self):
        return self.__domain_max


    @property
    def range_min(self):
        return self.__range_min


    @property
    def range_max(self):
        return self.__range_max


    @property
    def brightness(self):
        return self.__brightness


    @property
    def transition_time(self):
        return self.__transition_time


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ChromaConf:{domain_min:%s, domain_max:%s, range_min:%s, range_max:%s, " \
               "brightness:%s, transition_time:%s}" % \
               (self.domain_min, self.domain_max, self.range_min, self.range_max,
                self.brightness, self.transition_time)
