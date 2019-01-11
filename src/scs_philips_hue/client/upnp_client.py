"""
Created on 27 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

header:
CURLOPT_HTTPHEADER => array('Accept: application/json')

https://developers.meethue.com/news/
"""

import json

from collections import OrderedDict

from scs_core.sys.http_exception import HTTPException
from scs_core.sys.http_status import HTTPStatus

from scs_philips_hue.client.client_exception import ClientException


# --------------------------------------------------------------------------------------------------------------------

class UPnPClient(object):
    """
    classdocs
    """

    __HOST = "discovery.meethue.com"            # hard-coded URL
    __PATH = ""                                 # hard-coded URL

    # __HOST = "www.meethue.com"                # hard-coded URL
    # __PATH = "/api/nupnp"                     # hard-coded URL

    __HEADER_ACCEPT = "application/json"


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        """
        Constructor
        """
        self.__http_client = http_client


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self):
        self.__http_client.connect(self.__HOST)


    def close(self):
        self.__http_client.close()


    # ----------------------------------------------------------------------------------------------------------------

    def get(self):
        try:
            response_jstr = self.__http_client.get(self.__PATH, {}, self.__headers)
        except HTTPException as exc:
            if exc.status == HTTPStatus.NOT_FOUND:
                print("not found!")
                return []
            else:
                raise ClientException.construct(exc) from exc

        return json.loads(response_jstr, object_pairs_hook=OrderedDict)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def __headers(self):
        return {"Accept": UPnPClient.__HEADER_ACCEPT}


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
            return "UPnPClient:{http_client:%s}" % self.__http_client
