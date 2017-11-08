"""
Created on 5 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://en.wikipedia.org/wiki/Chromaticity
https://developers.meethue.com/documentation/core-concepts
"""

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ChromaSegment(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, start, end):
        """
        Constructor
        """
        self.__start = start                # ChromaPoint
        self.__end = end                    # ChromaPoint

        self.__delta_x = self.end.x - self.start.x
        self.__delta_y = self.end.y - self.start.y


    # ----------------------------------------------------------------------------------------------------------------

    def interpolate(self, intermediate):
        if not (0.0 <= intermediate <= 1.0):
            raise ValueError(intermediate)

        x = self.start.x + (self.__delta_x * intermediate)
        y = self.start.y + (self.__delta_y * intermediate)

        return ChromaPoint(x, y)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def start(self):
        return self.__start


    @property
    def end(self):
        return self.__end


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ChromaSegment:{start:%s, end:%s, delta_x:%0.4f, delta_y:%0.4f}" %  \
               (self.start, self.end, self.__delta_x, self.__delta_y)


# --------------------------------------------------------------------------------------------------------------------

class ChromaPoint(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def red(cls):
        return ChromaPoint(0.74, 0.26)


    @classmethod
    def green(cls):
        return ChromaPoint(0.08, 0.84)


    @classmethod
    def blue(cls):
        return ChromaPoint(0.17, 0.01)


    @classmethod
    def white_3000k(cls):
        return ChromaPoint(0.48, 0.41)


    @classmethod
    def white_6000k(cls):
        return ChromaPoint(0.32, 0.26)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jarray):
        if not jarray:
            return None

        x = jarray[0]
        y = jarray[1]

        return ChromaPoint(x, y)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, x, y):
        """
        Constructor
        """
        self.__x = round(float(x), 4)                   # float
        self.__y = round(float(y), 4)                   # float


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return [self.x, self.y]


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def x(self):
        return self.__x


    @property
    def y(self):
        return self.__y


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ChromaPoint:{x:%0.4f, y:%0.4f}" %  (self.x, self.y)
