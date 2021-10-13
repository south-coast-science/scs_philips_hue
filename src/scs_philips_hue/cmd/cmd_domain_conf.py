"""
Created on 16 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"topic-path": "/orgs/south-coast-science-demo/brighton/loc/1/particulates", "document-node": "val.pm10"}
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdDomainConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ [-t TOPIC_PATH] [-n DOCUMENT_NODE] | -x }] "
                                                    "[-i INDENT] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--topic", "-t", type="string", nargs=1, action="store", dest="topic_path",
                                 help="set the topic path")

        self.__parser.add_option("--node", "-n", type="string", nargs=1, action="store", dest="document_node",
                                 help="set the document node")

        self.__parser.add_option("--delete", "-x", action="store_true", dest="delete",
                                 help="delete the Chroma configuration")

        # output...
        self.__parser.add_option("--indent", "-i", type="int", nargs=1, action="store", dest="indent",
                                 help="pretty-print the output with INDENT")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete is not None:
            return False

        return True


    def is_complete(self):
        if self.topic_path is None or self.document_node is None:
            return False

        return True


    def set(self):
        return self.topic_path is not None or self.document_node is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic_path(self):
        return self.__opts.topic_path


    @property
    def document_node(self):
        return self.__opts.document_node


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def indent(self):
        return self.__opts.indent


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdDomainConf:{topic_path:%s, document_node:%s, delete:%s, indent:%s, verbose:%s}" % \
                    (self.topic_path, self.document_node, self.delete, self.indent, self.verbose)
