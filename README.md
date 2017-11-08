# scs_philips_hue
A light bulb moment.

How to control Philips Hue light bulbs from South Coast Science data sources.

The name Philips Hue is the property of its owner:
http://www2.meethue.com/en-gb


**Required libraries:** 

* Third party: paho-mqtt, pycurl
* SCS root: scs_core
* SCS host: scs_host_posix or scs_host_rpi


**Example PYTHONPATH:**

**Raspberry Pi, in /home/pi/.bashrc:**

export \\
PYTHONPATH=\~/SCS/scs_philips_hue:\~/SCS/scs_host_rpi:\~/SCS/scs_core:$PYTHONPATH


**MacOS, in ~/.bash_profile:**

PYTHONPATH="\{$HOME}/SCS/scs_philips_hue:\{$HOME}/SCS/scs_host_posix:\{$HOME}/SCS/scs_core:${PYTHONPATH}" \
export PYTHONPATH


**Ubuntu, in ~/.bashrc:**

export \\
PYTHONPATH="\~/SCS/scs_philips_hue:\~/SCS/scs_host_posix:\~/SCS/scs_core:$PYTHONPATH"
