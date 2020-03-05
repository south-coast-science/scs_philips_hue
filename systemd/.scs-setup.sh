#!/usr/bin/env bash

[ -f ~pi/scs-venv/bin/activate ] && . ~pi/scs-venv/bin/activate

# ****** IMPORTANT ******
# ******
# ****** Changes to this script must also be replicated in ~pi/.scs.env
# ******
# ****** IMPORTANT ******

export PYTHONPATH=/home/pi/SCS/scs_analysis/src:/home/pi/SCS/scs_core/src:/home/pi/SCS/scs_host_rpi/src:/home/pi/SCS/scs_philips_hue/src
