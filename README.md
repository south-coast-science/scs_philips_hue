# scs_philips_hue
A light bulb moment.

How to connect Philips Hue light bulbs to South Coast Science environmental data sources.

The name Philips Hue is the property of its owner:
http://www2.meethue.com/en-gb

_Contains command line utilities and library classes_


**Required libraries:** 

* Third party: paho-mqtt, pycurl
* SCS root: scs_core
* SCS host: scs_host_posix or scs_host_rpi


**Example PYTHONPATH:**

Raspberry Pi, in /home/pi/.bashrc:

    export PYTHONPATH=~/SCS/scs_philips_hue/src:~/SCS/scs_host_rpi/src:~/SCS/scs_core/src:$PYTHONPATH


macOS, in ~/.bash_profile:

    PYTHONPATH="{$HOME}/SCS/scs_philips_hue/src:{$HOME}/SCS/scs_host_posix/src:{$HOME}/SCS/scs_core/src:${PYTHONPATH}"
    export PYTHONPATH


Ubuntu, in ~/.bashrc:

    export PYTHONPATH="~/SCS/scs_philips_hue/src:~/SCS/scs_host_posix/src:~/SCS/scs_core/src:$PYTHONPATH"
