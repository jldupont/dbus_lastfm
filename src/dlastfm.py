#!/usr/bin/env python
"""
    DBus Lastfm 
    Start-up script

    @author: jldupont
"""
import os
import sys

# Adjust system path according to this script
cpath=os.path.dirname(__file__)
sys.path.append(cpath)

from dbus_lastfm import main #@UnresolvedImport

main()