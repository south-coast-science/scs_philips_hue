"""
Created on 7 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"lastscan": "2017-11-07T12:10:47", "1": {"name": "Hue color lamp 1"}}
"""

from scs_core.data.json import JSONable

from scs_philips_hue.data.light.light_name import LightName


# --------------------------------------------------------------------------------------------------------------------

class LightScan(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        last_scan = None
        lights = []

        for index, value in jdict.items():
            if index == 'lastscan':
                last_scan = value
            else:
                lights.append({index: LightName.construct_from_jdict(value)})

        return LightScan(last_scan, lights)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, last_scan, lights):
        """
        Constructor
        """
        self.__last_scan = last_scan                # string (may be date / time)
        self.__lights = lights                      # array of LightAttribute


    # ----------------------------------------------------------------------------------------------------------------

    def is_active(self):
        return self.last_scan == 'active'


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = []

        jdict['lastscan'] = self.last_scan

        for index, light in self.lights.items():
            jdict[index] = light

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def last_scan(self):
        return self.__last_scan


    @property
    def lights(self):
        return self.__lights


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        lights = '{' + ', '.join(str(index) + ': ' + str(light) for index, light in self.lights.items()) + '}'

        return "LightScan:{last_scan:%s, lights:%s}" %  (self.last_scan, lights)
