"""
Created on 29 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_philips_hue.config.bridge_address import BridgeAddress, BridgeAddressSet
from scs_philips_hue.config.bridge_credentials import BridgeCredentialsSet

from scs_philips_hue.discovery.discovery import Discovery

from scs_philips_hue.manager.bridge_manager import BridgeManager


# --------------------------------------------------------------------------------------------------------------------

class BridgeBuilder(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_for_name(cls, bridge_name):
        logger = Logging.getLogger()

        # credentials...
        credentials_set = BridgeCredentialsSet.load(Host)

        try:
            credentials = credentials_set.credentials(bridge_name)
            logger.info(credentials)

        except KeyError:
            logger.error("no stored credentials for bridge '%s'." % bridge_name)
            exit(1)

        # cached address?..
        address_set = BridgeAddressSet.load(Host, skeleton=True)

        try:
            address = address_set.address(bridge_name)
            return BridgeManager(address.ipv4.dot_decimal(), credentials.username)

            # TODO: check that that the cached address is valid

        except KeyError:
            logger.info("no cached IP address...")

        # find bridge...
        discovery = Discovery(Host)
        bridge = discovery.find(credentials)

        if bridge is None:
            logger.error("stored credentials are not valid for bridge '%s'." % bridge_name)
            exit(1)

        # add address...
        address_set.add(BridgeAddress.construct(bridge_name, bridge.ip_address))
        address_set.save(Host)

        return BridgeManager(bridge.ip_address, credentials.username)
