#!/usr/bin/env python3

"""
Created on 9 Nov 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Generate a list of scripts that may be included in setup.py
"""

import os

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

local_path = os.path.join('src', 'scs_philips_hue')
abs_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), local_path)

for item in Filesystem.ls(abs_path):
    if not item.is_directory and (item.has_suffix('py') or item.has_suffix('sh')) and not item.name.startswith('__'):
        print("        '" + os.path.join(local_path, item.name) + "',")
