"""
Created on 30 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_philips_hue.client.rest_client import RESTClient


# --------------------------------------------------------------------------------------------------------------------

class Manager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, host, username):
        """
        Constructor
        """
        self._rest_client = RESTClient(http_client)

        self._host = host
        self._username = username


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        classname = self.__class__.__name__

        return classname + ":{rest_client:%s, host:%s, username:%s}" % (self._rest_client, self._host, self._username)
