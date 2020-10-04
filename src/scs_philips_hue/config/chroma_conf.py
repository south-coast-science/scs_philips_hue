"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"min": {"domain-min": 0, "range-min": [0.05, 0.5]},
"intervals": [{"domain-max": 27, "range-max": [0.07, 0.82]}, {"domain-max": 53, "range-max": [0.38, 0.6]},
{"domain-max": 80, "range-max": [0.48, 0.51]}, {"domain-max": 101, "range-max": [0.52, 0.47]},
{"domain-max": 121, "range-max": [0.56, 0.43]}, {"domain-max": 136, "range-max": [0.62, 0.36]},
{"domain-max": 151, "range-max": [0.72, 0.26]}, {"domain-max": 173, "range-max": [0.55, 0.17]},
{"domain-max": 180, "range-max": [0.4, 0.21]}], "brightness": 254, "transition-time": 1}

https://docs.python.org/3.5/howto/sorting.html#odd-and-ends
"""

import os

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable, PersistentJSONable

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
    def persistence_location(cls, host):
        return os.path.join(host.scs_dir(), cls.__DIR), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        minimum = ChromaMin.construct_from_jdict(jdict.get('min'))

        intervals = []
        for interval_jdict in jdict.get('intervals'):
            intervals.append(ChromaInterval.construct_from_jdict(interval_jdict))

        brightness = jdict.get('brightness')
        transition_time = jdict.get('transition-time')

        return ChromaConf(minimum, intervals, brightness, transition_time)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, minimum, intervals, brightness, transition_time):
        """
        Constructor
        """
        super().__init__()

        self.__minimum = minimum                                # ChromaMin
        self.__intervals = intervals                            # array of ChromaInterval

        self.__brightness = Datum.int(brightness)               # int
        self.__transition_time = Datum.int(transition_time)     # int


    def __len__(self):
        return len(self.__intervals)


    # ----------------------------------------------------------------------------------------------------------------

    def has_interval(self, domain_max):
        for i in range(len(self.__intervals)):
            if self.__intervals[i].domain_max == domain_max:
                return True

        return False


    def insert_interval(self, interval):
        # update existing...
        for i in range(len(self.__intervals)):
            if self.__intervals[i].domain_max == interval.domain_max:
                self.__intervals[i] = interval
                return

        # or insert new...
        self.__intervals.append(interval)
        self.__intervals.sort()


    def remove_interval(self, domain_max):
        # remove existing...
        for i in range(len(self.__intervals)):
            if self.__intervals[i].domain_max == domain_max:
                del self.__intervals[i]
                return


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['min'] = self.minimum
        jdict['intervals'] = self.intervals

        jdict['brightness'] = self.brightness
        jdict['transition-time'] = self.transition_time

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def minimum(self):
        return self.__minimum


    @property
    def intervals(self):
        return self.__intervals


    @property
    def brightness(self):
        return self.__brightness


    @property
    def transition_time(self):
        return self.__transition_time


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        intervals = [str(interval) for interval in self.__intervals]

        return "ChromaConf:{minimum:%s, intervals:%s, brightness:%s, transition_time:%s}" % \
               (self.minimum, intervals, self.brightness, self.transition_time)


# --------------------------------------------------------------------------------------------------------------------

class ChromaMin(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        domain_min = jdict.get('domain-min')
        range_min = ChromaPoint.construct_from_jdict(jdict.get('range-min'))

        return ChromaMin(domain_min, range_min)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, domain_min, range_min):
        """
        Constructor
        """
        super().__init__()

        self.__domain_min = int(round(domain_min, 0))           # int
        self.__range_min = range_min                            # ChromaPoint


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['domain-min'] = self.domain_min
        jdict['range-min'] = self.range_min

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def domain_min(self):
        return self.__domain_min


    @property
    def range_min(self):
        return self.__range_min


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ChromaMin:{domain_min:%s, range_min:%s}" % (self.domain_min, self.range_min)


# --------------------------------------------------------------------------------------------------------------------

class ChromaInterval(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        domain_max = jdict.get('domain-max')
        range_max = ChromaPoint.construct_from_jdict(jdict.get('range-max'))

        return ChromaInterval(domain_max, range_max)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, domain_max, range_max):
        """
        Constructor
        """
        super().__init__()

        self.__domain_max = int(round(domain_max, 0))           # int
        self.__range_max = range_max                            # ChromaPoint


    def __lt__(self, other):
        return self.domain_max < other.domain_max


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['domain-max'] = self.domain_max
        jdict['range-max'] = self.range_max

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def domain_max(self):
        return self.__domain_max


    @property
    def range_max(self):
        return self.__range_max


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ChromaInterval:{domain_max:%s, range_max:%s}" % (self.domain_max, self.range_max)
