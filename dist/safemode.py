# --------------------------------------
# Project          : MagTag Data Logger
# Version          : 0.1
# Date             : 02 Mar 2023
# Author           : OneOfTheInfiniteMonkeys
# Copyright        : (c) Copyright OneOfTheInfiniteMonkeys All Rights Reserved
# Source Location  : https://github.com/OneOfTheInfiniteMonkeys/MTDL
# License          : MIT License - See distribution licence details
#                  : Applicable to only those elements authored by OneOfTheInfiniteMonkeys
# Hardware         : Adafruit MagTag
# --------------------------------------#
# safemode.py
# Needs CircuitPython 8.1.x and later
# https://learn.adafruit.com/circuitpython-safe-mode/safemode-py
#
# Actions for power brown out othewise report to console

import microcontroller
import supervisor

if supervisor.runtime.safe_mode_reason == supervisor.SafeModeReason.BROWNOUT:
    microcontroller.reset()    # Reset and start over.
    
# Otherwise, do nothing. The safe mode reason will be printed in the
# console, and nothing will run.