#!/usr/bin/env python3

"""
Created on 21 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_philips_hue

DESCRIPTION
The osio_client_auth utility is used to store or read the client ID and client password required by the OpenSensors.io
Community Edition messaging system. This client authentication is required to subscribe to any messaging topic.

When setting the client authentication, the osio_client_auth utility requests a new device identity from the
OpenSensors system, then stores the generated tokens on the client. The name of the device is taken to be the
name of the host on which the script is executed. Names (unlike client IDs) are not required to be unique on the
OpenSensors system.

SYNOPSIS
osio_client_auth.py [-u USER_ID] [-l LAT LNG POSTCODE] [-v]

EXAMPLES
./osio_client_auth.py -u south-coast-science-demo-user -l 50.823130 -0.122922 "BN2 0DF" -v

FILES
~/SCS/osio/osio_client_auth.json

DOCUMENT EXAMPLE
{"user_id": "southcoastscience-dev", "client-id": "5403", "client-password": "rtxTrK2f"}

SEE ALSO
scs_philips_hue/osio_api_auth
scs_philips_hue/osio_mqtt_subscriber
"""

import sys

from scs_core.client.http_client import HTTPClient

from scs_core.data.json import JSONify

from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.client.client_auth import ClientAuth
from scs_core.osio.config.project_source import ProjectSource
from scs_core.osio.manager.device_manager import DeviceManager
from scs_core.osio.manager.user_manager import UserManager

from scs_core.sys.system_id import SystemID

from scs_host.sys.host import Host

from scs_philips_hue.cmd.cmd_osio_client_auth import CmdOSIOClientAuth


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    system_id = SystemID('scs', 'phi', 'Hue Interface', 'RPi', Host.name())

    description = 'South Coast Science - Philips Hue Bridge'
    tags = ['scs', 'philips-hue']


    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOClientAuth()

    if cmd.verbose:
        print("osio_client_auth: %s" % cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # APIAuth...
    api_auth = APIAuth.load(Host)

    if api_auth is None:
        print("osio_client_auth: APIAuth not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print("osio_client_auth: %s" % api_auth, file=sys.stderr)

    # HTTPClient...
    http_client = HTTPClient(False)

    # User manager...
    user_manager = UserManager(http_client, api_auth.api_key)

    # Device manager...
    device_manager = DeviceManager(http_client, api_auth.api_key)

    # check for existing registration...
    device = device_manager.find_for_name(api_auth.org_id, system_id.box_label())


    # ----------------------------------------------------------------------------------------------------------------
    # validate...

    # TODO: check whether remote device and local client auth match

    if device is None:
        if cmd.set() and not cmd.is_complete():
            print("osio_client_auth: No device is registered. You must therefore set a user and location:",
                  file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(1)

        if not cmd.set():
            exit(0)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        # User...
        if cmd.user_id:
            user = user_manager.find_public(cmd.user_id)

            if user is None:
                print("osio_client_auth: User not available.", file=sys.stderr)
                exit(1)

        # device...
        if device:
            if cmd.user_id:
                print("osio_client_auth: device owner-id cannot be updated.", file=sys.stderr)
                exit(1)

            # find ClientAuth...
            client_auth = ClientAuth.load(Host)

            # update Device...
            updated = ProjectSource.update(device, cmd.lat, cmd.lng, cmd.postcode, description, tags)
            device_manager.update(api_auth.org_id, device.client_id, updated)

            # find updated device...
            device = device_manager.find(api_auth.org_id, device.client_id)

        else:
            # create Device...
            device = ProjectSource.create(system_id, api_auth, cmd.lat, cmd.lng, cmd.postcode, description, tags)
            device = device_manager.create(cmd.user_id, device)

            # create ClientAuth...
            client_auth = ClientAuth(cmd.user_id, device.client_id, device.password)

            client_auth.save(Host)

    else:
        # find ClientAuth...
        client_auth = ClientAuth.load(Host)

    if cmd.verbose:
        print("osio_client_auth: %s" % client_auth, file=sys.stderr)

    print(JSONify.dumps(device))
