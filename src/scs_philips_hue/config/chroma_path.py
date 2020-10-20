"""
Created on 4 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"name": "test", "points": [[0.74, 0.26], [0.48, 0.41], [0.08, 0.84]]}
"""

import os

from collections import OrderedDict

from scs_core.data.json import MultiPersistentJSONable
from scs_core.data.str import Str

from scs_core.sys.filesystem import Filesystem

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

    __FILENAME =          "chroma_path.json"

    @classmethod
    def persistence_location(cls, name):
        filename = cls.__FILENAME if name is None else '_'.join((name, cls.__FILENAME))

        return cls.hue_dir(), filename


    @classmethod
    def defaults(cls):
        archive = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'paths')
        paths = Filesystem.ls(archive)

        return [path.name.split('.')[0] for path in paths]


    @classmethod
    def load_default(cls, name):
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'paths', '.'.join((name, 'json')))

        if not os.path.exists(file):
            raise FileNotFoundError(name)

        return cls.load_from_file(file)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, name=None):
        if not jdict:
            return None

        points = [ChromaPoint.construct_from_jdict(point_jdict) for point_jdict in jdict.get('points')]

        return cls(points, name=name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, points, name=None):
        """
        Constructor
        """
        super().__init__(name)

        self.__points = points                      # array of ChromaPoint


    def __len__(self):
        return len(self.points)


    # ----------------------------------------------------------------------------------------------------------------

    def range_min(self):
        if not len(self):
            return None

        return self.__points[0]


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
    def points(self):
        return self.__points


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ChromaPath:{name:%s, points:%s}" % (self.name, Str.collection(self.__points))
