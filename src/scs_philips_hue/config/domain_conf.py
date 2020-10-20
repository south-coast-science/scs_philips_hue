"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"topic-path": "/orgs/south-coast-science-demo/brighton/loc/1/particulates", "document-node": "val.pm10"}
"""

import os

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class DomainConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME =        "domain_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.hue_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        topic_path = jdict.get('topic-path')
        document_node = jdict.get('document-node')

        return cls(topic_path, document_node)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic_path, document_node):
        """
        Constructor
        """
        super().__init__()

        self.__topic_path = topic_path                          # string
        self.__document_node = document_node                    # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['topic-path'] = self.topic_path
        jdict['document-node'] = self.document_node

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic_path(self):
        return self.__topic_path


    @property
    def document_node(self):
        return self.__document_node


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DomainConf:{topic_path:%s, document_node:%s}" % (self.topic_path, self.document_node)
