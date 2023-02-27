"""><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><-->
# --------------------------------------
# Project          : MacroPad
# Version          : 0.9
# Date             : 27 Feb 2023
# Author           : OneOfTheInfiniteMonkeys
# Copyright        : (c) Copyright OneOfTheInfiniteMonkeys All Rights Reserved
# Source Location  : https://github.com/OneOfTheInfiniteMonkeys/MTDL
# License          : MIT License - See distribution licence details
#                  : Applicable to only those elements authored by OneOfTheInfiniteMonkeys
# Hardware         : Adafruit MagTag
# --------------------------------------
#                  :
# From             : Various and new code
# --------------------------------------
# Trademarks       : As owned by the respective registrants
# -------><--------><--------><--------><--------><--------><--------><-------->
"""
#import microcontroller                  # Allow access to internal temperature
import board                             # Allow access to DISPLAY
import alarm                             # NV Ram access and wakeup alarm types
#import rtc                              # For the system clock setting
import time                              # access sleep function
#import wifi                             # Access to MAC id for a unique id
#import socketpool                       # Used to access network sockets
#import ssl                              # Secure Socket Layer protocol support
# import adafruit_requests               # Requests-like library for web interfacing
#import json                             # Support for JSON handling
import displayio                         # For bitmap image display
import adafruit_imageload                # Support for bitmap image loading of icons
import sys                               # System version information
import os                                # Allow access to board id, CircuitPython version
import supervisor                        # Allows detection of USB connected state
from adafruit_magtag.magtag import MagTag # Wrapper for lower level board features - Network Graphics Peripherals
#
# --------------------------------------
# function list
# --------------------------------------
# interpreter_ver()
# interpreter_nam()
# nv_store_write_str(StrToStore, Location)
# nv_store_read_str(Location)
# set_mt_leds(ldclr, lbl)
# count_neopixel(sel_mode, ldclr, lbl, magtag):
# load_vlt_icon(lvl, magtag)
# load_wif_icon(lvl, magtag)
# load_small_icon(icon_file_name, xpos, magtag)
# button_read(magtag)
# average_light(magtag)
# light_boost_level_factor(LightLevel)
# light_boost_level(LightLevel)
# pause_or_press(magtag, delay_period)
# while_display_busy(delay_period)
# battery_check(sv, lpsp, mt_idx, magtag)
# current_battery_level(sv)
# deepsleepmode(magtag, mt_idx)
# hh_mm(time_struct, twelve_hour)
# USB_connected()
# --------------------------------------

# --------------------------------------
# Colour definitions
# --------------------------------------
# Neopixel Colours - Order R G B as RRGGBB
RED = 0xFF0000
AMBER = 0xAA9900
BLUE = 0x0066FF
MAGENTA = 0xFF00FF
PURPLE = 0x3B0F85
ORANGE = AMBER
BLACK = 0x000000
LOW_RED = 0x040000
LOW_GREEN = 0x000400
LOW_BLUE = 0x000004
LOW_WHITE = 0x020202
LOW_YELLOW = 0x020200
# --------------------------------------

# ------------------------------------------------------------------------------
def interpreter_ver():
    """
    # --------------------------------------
    # Return CirctuitPython interpreter version as a string with decimal separators
    # --------------------------------------
    """
    return ".".join(map(str, sys.implementation[1]))
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def interpreter_nam():
    """
    # --------------------------------------
    # Return CirctuitPython interpreter name as a string
    # --------------------------------------
    """
    return "".join(map(str, sys.implementation[0]))
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def nv_store_write_str(StrToStore, Location):
    """
    # --------------------------------------
    # Store a string to the battery backed memory (not EEPROM)
    """
    i = 0
    byteArray = bytes(StrToStore, 'ascii')
    # We only need to write length bytes of the string
    for i in range(len(StrToStore)):
        alarm.sleep_memory[Location + i] = byteArray[i]
    # <-- End of iteration transferring data into sleep memory

    # We need to terminate the string in the storage with a zero
    i += 1
    alarm.sleep_memory[Location + i] = 0
    return
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def nv_store_read_str(Location):
    """
    # --------------------------------------
    # Retrieve a string from the battery backed memory (not EEPROM)
    # The string is zero (null) terminated in the memory
    # The input parameter is a memory location previously written
    """
    # Read from the specified location and return the string obtained
    i = 0                         # Initialise a counter
    StrToStore = ""               # Initialise string storage
    while (alarm.sleep_memory[Location + i] != 0):
        StrToStore += chr(alarm.sleep_memory[Location + i])  # build the string
        i += 1                    # Increment the counter to point at next byte
        # <-- End of loop reading from sleep memory
    return StrToStore  # return the string read from the memory location
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def set_mt_leds(ldclr, lbl, magtag):
    """
    # --------------------------------------
    # Set LED's to colour and intensity
    # --------------------------------------
    """
    if (lbl == 0):  #  Ensure light booster level is non zero so LED is active
        lbl = 4
    magtag.peripherals.neopixels[3] = (ldclr) * lbl  # colour * brightness
    magtag.peripherals.neopixels[2] = (ldclr) * lbl
    magtag.peripherals.neopixels[1] = (ldclr) * lbl
    magtag.peripherals.neopixels[0] = (ldclr) * lbl
    return
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def count_neopixel(sel_mode, ldclr, lbl, magtag):
    """
    # --------------------------------------
    # Set the LED's at the top of the MagTag to show the binary value of the
    # integer parameter sel_mode. The range is 0 to 0x0F or 16 decimal
    # Accommodates LED numbering from right to left
    # 3 parameters:
    #   sel_mode - integer, range 0 to 0x0F or 16 decimal
    #   ldclr    - integer, range 0x000001 to 0x0F0000
    #   lbl      - integer, range 0 to 16 representing light boost level
    """
    magtag.peripherals.neopixels.fill(0x000000)
    if (ldclr == 0):
        ldclr = 0x000800  # Default to green where no colour selected
    if (ldclr > 0x0F0000):
        ldclr = 0x0F0000  # Accommodate colour and light level boost feature
    if (lbl < 1):
        lbl = 1    # Always have at least some boost so as not to multiply by 0
    if (sel_mode > 0):  #  Don't write a colour if sel_mode is zero
        if (sel_mode & 1):
            magtag.peripherals.neopixels[3] = (ldclr) * lbl  # colour * brightness
        if (sel_mode & 2):
            magtag.peripherals.neopixels[2] = (ldclr) * lbl
        if (sel_mode & 4):
            magtag.peripherals.neopixels[1] = (ldclr) * lbl
        if (sel_mode & 8):
            magtag.peripherals.neopixels[0] = (ldclr) * lbl
    return
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def load_vlt_icon(lvl, magtag):
    # Display the battery voltage level icon based on an assessed battery level
    # The terminal discharge voltage is non linear
    # sv = Current_Battery_Level(lvl)
    load_small_icon("bat0" + str(lvl) + ".bmp", 274, magtag)
    return
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def load_wif_icon(lvl, magtag):
    sv = 6
    load_small_icon("wif0" + str(sv) + ".bmp", 258, magtag)
    return
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def load_small_icon(icon_file_name, xpos, magtag):
    # uses small_icon_class
    # loads from a file into the Tile Grid at the x position specified at the top of the display
    icons_small_bmp, icons_small_pal = adafruit_imageload.load("/ico/" + icon_file_name)
    small_icon_class = displayio.TileGrid(
                                    icons_small_bmp,
                                    pixel_shader=icons_small_pal,
                                    x=xpos,
                                    y=0,
                                    width=1,
                                    height=1,
                                    tile_width=16,
                                    tile_height=16,
                                   )

    small_ico_class = displayio.Group()
    small_ico_class.append(small_icon_class)
    magtag.splash.append(small_ico_class)
    return
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def button_read(magtag):
    """
    # --------------------------------------
    # Reads the MagTag buttons and returns an integer representing the
    # combination of buttons pressed
    # combination of buttons pressed
    # No buttons pressed = 0 all buttons pressed = 15
    """
    # bpv = Button Pressed Value
    bpv = int(not magtag.peripherals.buttons[0].value)
    bpv += int(not magtag.peripherals.buttons[1].value)*2
    bpv += int(not magtag.peripherals.buttons[2].value)*4
    bpv += int(not magtag.peripherals.buttons[3].value)*8

    return bpv                 # return a value representing the buttons pressed
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def average_light(magtag):
    """
    # --------------------------------------
    # Reads the MagTag light sensors and returns an integer representing the
    # average light level over a sample period
    """
    NoOfIterations = 2                              # Number of iterations to perform
    i = 0                                           # loop counter
    oll = magtag.peripherals.light                  # oll = Old Light Level
    lla = 0                                         # lla = Light Level Average
    while (i < NoOfIterations):
        # Exponential filter
        lla = (0.7 * magtag.peripherals.light) + (0.3 * oll)
        oll = lla
        i += 1
        time.sleep(0.05)
    # <-- End Of While loop
    # print("Light Level Average:" + str(lla))
    # return an integer value representing the averaged light level
    return int(lla)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def light_boost_level_factor(LightLevel):
    """
    # --------------------------------------
    # Calculate the Light boost level based on the provided Light Level
    # taken from a light sensor, or possibly derived from time of day etc.
    # Colours can be multiplied by the boost level to increase the brightness
    # such that RGB 00 00 08 becomes RGB 00 00 10 when multiplied by 2
    # Note:
    #   Values shown above in hex
    #   The boost points are empirically selected
    """
    # bl = Boost Level
    bl = 1
    if (LightLevel >= 500):
        bl = 2
    if(LightLevel >= 750):
        bl = 4
    if(LightLevel >= 2000):
        bl = 6
    if(LightLevel >= 3000):
        bl = 8
    if(LightLevel >= 5000):
        bl = 10
    if(LightLevel >= 6000):
        bl = 16
    # print("Light Boost Level  :" + str(bl))
    return int(bl)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def light_boost_level(LightLevel):
    """
    # --------------------------------------
    # Wraps measuring the light level and scaling to an integer boost level
    """
    return light_boost_level_factor(LightLevel)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def pause_or_press(magtag, delay_period):
    """
    # --------------------------------------
    # Pauses unless key pressed returns key pressed value
    # Flashing one of the NEOPIXEL LED's
    # The delay period should be at least 1 second
    """
    # Allow the user chance to press any button on the front of the MagTag
    i = 0                                                     # Loop counter
    b = 0                                                     # Will be button pressed value
    end_period = delay_period * 10                            # Convert delay_period to sleep counts
    while ((i <= end_period) & (b == 0)):
        i += 1                                                # Increment the counter
        b = button_read(magtag)                                  # Read all buttons and return a value
        time.sleep(0.1)                                       # We don't need to sample too quickly
    return int(b)                                             # return the button pressed 0 if none pressed
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def while_display_busy(delay_period):
    """
    # --------------------------------------
    # Monitor the display, as it might complete early otherwise exit if the delay period expires
    # normally the returned value will reflect that the display completed updating sooner than
    # the allowed delay_period
    """
    display = board.DISPLAY                                   # permit access to the display device (e-ink)
    i = 0                                                     # Loop counter
    d = 1                                                     # Will be display status returned
    if (delay_period < 2):                                    # Ensure display_period is at least 2 seconds
        delay_period = 2
    end_period = delay_period * 10                            # Convert delay_period to sleep counts
    while ((i <= end_period) & (d == 1)):                     # Loop until display completes or count expires
        i += 1                                                # Increment the counter
        time.sleep(0.1)                                       # We don't need to sample too quickly
        d = display.busy                                      # Read display status
    return d                                                  # return the display status
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def battery_check(sv, lpsp, mt_idx, magtag):
    """
    # --------------------------------------
    # Checks the battery level and display a warning if too low.
    # Voltage cut off for:
    # PKCELL LP402025  150 mAh 3.7 V Li.Poly - No Applicable
    # PKCELL LP503035  500 mAh 3.7 V Li.Poly
    # PKCELL LP503562 1200 mAh 3.7 V Li.Poly
    # PKCELL LP803860 2000 mAh 3.7 V Li.Poly - No Applicable
    # PKCELL LP605080 3000 mAh 3.7 V Li.Poly - No Applicable
    # Voltage range from 4.2 Volts fully charged to 3.7 Volts
    # We are working to just above 88% of 4.2 Volts based on acquired data
    # To permit the power LED not to fully exhaust the battery
    """
    # sv = SystemVoltage
    if (sv <= 3.74):
        magtag.graphics.set_background("/bmps/magtag-pl-01.bmp")  # Show Power on graphic - battery empty
        magtag.set_text("Battery Low!     " + "{:.2f}".format(sv) + " Volts", mt_idx, auto_refresh=True )
        d = while_display_busy(3)                                 # Allow display to complete update
        d = pause_or_press(magtag, 5)                             # Pause and allow a key press

    # If battery really low then sleep to protect the battery
    if (sv < 3.71):                                               # 83% of 3.7 Volts - Assume Power LED draws 40 uA
        magtag.graphics.set_background("/bmps/magtag-pl-01.bmp")  # Show a Power on graphic - battery empty
        magtag.set_text("Recharge now!     " + "{:.2f}".format(sv) + " Volts", mt_idx, auto_refresh=True )
        d = while_display_busy(3)                                 # Allow display to complete update
        magtag.exit_and_deep_sleep(lpsp)                          # Basically don't wake again - well ~ 1 month
    return
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def Current_Battery_Level(sv):
    """
    # --------------------------------------
    # Assign a battery level to the voltage
    # Returns an integer  level classification
    # e.g. for battery icon selection
    # Levels adjusted for 2000 mAh cell characterisation
    # sv = System Voltage
    # bl = Battery Level
    # 4.20 Volts a battery is charged - 4.30 volts no battery fitted
    # --------------------------------------
    """
    if (sv >= 4.25):
        bl = 6
    if (sv < 4.25):
        bl = 5
    if (sv < 4.04):
        bl = 4
    if (sv < 4.00):
        bl = 3
    if (sv < 3.90):
        bl = 2
    if (sv < 3.83):
        bl = 1
    if (sv < 3.72):
        bl = 0
    # print("System voltage     :" + "{:.1f}".format(sv) +
    #      " Volts " + " Bat. Level " + str(bl))
    return int(bl)                           # Return the assessed battery level
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def strpad(inpstr, strlength):
    """
    # Return a padded string of length strlength by adding trailing spaces
    #
    """
    while (len(inpstr) < strlength):
      inpstr += " "
    if (len(inpstr) > strlength):
        inpstr = inpstr[:strlength]  #                      slice the string to length
    return inpstr
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def timestr(secs):
    """
    # Return a time str based on the number of seconds provided
    # Returned string is hhhh:mm
    # Note there are 8760 hours in a year
    # Typical use is to offset a time by n seconds
    """
    sec_value = secs % (24 * 3600)
    hour_value = sec_value // 3600
    sec_value %= 3600
    min_value = sec_value // 60
    sec_value %= 60
    timestring = "{:04d}".format(int(hour_value)) + ":" + "{:02d}".format(int(min_value))
    return timestring
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def deepsleepmode(LBL, mt_idx, magtag):
    """
    # --------------------------------------
    # Place instructions on the screen and enter deep sleep mode
    """
    magtag.peripherals.neopixels[0] = LOW_YELLOW * LBL  #       Yellow - Not sending key presses
    magtag.set_text("Off", mt_idx, auto_refresh = False)
    mt_idx = magtag.add_text(
                             # Use default small system font
                             # text_position = (108, 120),
                             text_position = (8, 134),
                             line_spacing = 0.8,
                             text_wrap = 20
                            )
    magtag.graphics.set_background("/bmps/magtag-basic-00.bmp")  # Load background graphic
    AboutTxt = strpad("Press reset button to activate.", 40)
    AboutTxt = strpad("MagTag Data Logger",20)
    AboutTxt += strpad(" ", 20)
    AboutTxt += strpad("Written by",20)
    AboutTxt += strpad(" ", 20)
    AboutTxt += strpad("   OneOfTheInfinite",20)
    AboutTxt += "        Monkeys"
    AboutTxt += strpad(" ", 32) # align to left of screen
    AboutTxt += strpad(" ", 60)
    AboutTxt += "Board    : " + strpad(os.uname().sysname, 9)
    AboutTxt += strpad("uf2 Ver. : " + str(os.uname().version), 40)
    magtag.set_text(AboutTxt, mt_idx, auto_refresh = True)  #   Set the display
    AboutTxt =""  #                                             Manage memory space
    d = while_display_busy(3)  #                                Allow display to complete update
    magtag.peripherals.neopixels[0] = BLACK  #                  No lights - Not sending key presses
    magtag.exit_and_deep_sleep(2678400)  #                      Basically don't wake again - well ~ 1 month
    return
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
def hh_mm(time_struct, twelve_hour=True):
    """ Given a time.struct_time, return a string as H:MM or HH:MM, either
        12- or 24-hour style depending on twelve_hour flag.
    """
    postfix = ""
    if twelve_hour:
        if time_struct.tm_hour > 12:
            hour_string = str(time_struct.tm_hour - 12) # 13-23 -> 1-11 (pm)
            postfix = "p"
        elif time_struct.tm_hour > 0:
            hour_string = str(time_struct.tm_hour) # 1-12
            postfix = "a"
        else:
            hour_string = '12' # 0 -> 12 (am)
            postfix = "a"
    else:
        hour_string = '{hh:02d}'.format(hh=time_struct.tm_hour)
    return hour_string + ':{mm:02d}'.format(mm=time_struct.tm_min) + postfix
# ------------------------------------------------------------------------------

def USB_Connected():
    # Needs import supervisor - first use CP 8.0.1
    # Returns True or False
    return supervisor.runtime.usb_connected

# --------------------------------------
#
# --------------------------------------
# End of code
# --------------------------------------
"""
# --------------------------------------
#
# --------------------------------------
2023-02-23 - 0.91
             Style improvement - return statement consistently applied to all functions
             Source location comment updated from MTMP to MTDL
             
2023-02-22 - 0.9
             Typo corrections
             Battery voltage level assessment issue correction
             
2023-02-21 - 0.8
             Updated battery voltage indication levels based on characterised Battery Discharge Curve

2023-02-16 - 0.7
             Added USB_Connected
             Reduced debug print output text

2023-02-03 - 0.6
             load_small_icon modified:
               Status bar icons moved to /ico/ folder
               Modified displayio.Group() to remove parameter issue with CirctuitPython 7.x
             added hh_mm from Adafruit MagTag cat feeder


2023-01-30 - 0.1 - Development Starts
# --------------------------------------
"""
