"""
Created on 4 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"name": "test", "points": [[0.74, 0.26], [0.48, 0.41], [0.08, 0.84]]}
"""

import os

from collections import OrderedDict

from scs_core.data.json import MultiPersistentJSONable

from scs_philips_hue.data.light.chroma import ChromaPoint


# --------------------------------------------------------------------------------------------------------------------

class ChromaPath(MultiPersistentJSONable):
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
    __PREFIX =          "chroma_path_"

    @classmethod
    def persistence_location(cls, host, name):
        return os.path.join(host.scs_dir(), cls.__DIR), cls.__PREFIX + name + '.json'


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        name = jdict.get('name')
        points = [ChromaPoint.construct_from_jdict(point_jdict) for point_jdict in jdict.get('points')]

        return ChromaPath(name, points)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, points):
        """
        Constructor
        """
        self.__name = name                          # string
        self.__points = points                      # array of ChromaPoint


    def __len__(self):
        return len(self.points)


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        self.save_to_file(*self.persistence_location(host, self.name))


    # ----------------------------------------------------------------------------------------------------------------

    def has_point(self, index):
        return index in range(len(self))


    def insert_point(self, index, point):
        self.__points.insert(index, point)          # may raise IndexError


    def remove_point(self, index):
        self.__points.pop(index)                    # may raise IndexError


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['name'] = self.name
        jdict['points'] = self.points

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    @property
    def points(self):
        return self.__points


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        points = ', '.join(str(point) for point in self.__points)

        return "ChromaPath:{name:%s, points:[%s]}" % (self.name, points)
