"""><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><--><-->
# --------------------------------------
# Project          : Logger
# Version          : 0.1
# Date             : 27 Feb 2023
# Author           : OneOfTheInfiniteMonkeys
# Copyright        : (c) Copyright OneOfTheInfiniteMonkeys All Rights Reserved
# Source Location  : https://github.com/OneOfTheInfiniteMonkeys/MTDL
# License          : MIT License - See distribution licence details
#                  : Applicable to only those elements authored by OneOfTheInfiniteMonkeys
# Hardware         : Adafruit MagTag
# CircuitPython    : 8.0.x
# --------------------------------------
#                  :
# From             : https://github.com/OneOfTheInfiniteMonkeys/MTDL
# --------------------------------------
# Trademarks       : As owned by the respective registrants
# -------><--------><--------><--------><--------><--------><--------><-------->
#
#
#
# --------------------------------------
# Magtag           :
#   Display size   : 296 x 128
#   Disp. Colours  : 0x000000, 0x666666, 0x999999, 0xFFFFFF
# --------------------------------------
"""
import time #                                               For Alarm functions and watchdog
import board #                                              For Alarm functions
import alarm #                                              For Alarm functions
import os #                                                 Environment access
import helper as hlp  #                                     Helper routines
import adafruit_lis3dh #                                    Temperature / Vibe sensor access
from adafruit_magtag.magtag import MagTag #                 MagTag
from adafruit_display_shapes.line import Line #             Line drawing library
import adafruit_minimqtt.adafruit_minimqtt as MQTT #        For posting data to the web
import ssl #                                                MQQT access - Secure Socket Layer to secure data transfer
import socketpool #                                         MQQT access - TCP/IP socket management for MQQT data tfr
import wifi #                                               MQQT access - WiFi access for MQQT conversation
import ipaddress #                                          Allows for optional (and poss. lower power) static ip address
from secrets import secrets #                               Access the secrets.py

import microcontroller #                                    For watchdog timer
import watchdog #                                           For watchdog timer

#---------------------------------------
# Initialise defaults
Data_Lg_S_Cnt = 5 #                                         >=1 : Count of Display Update periods before entering data into log
Dis_Upd_Prd = 120 #                                         >=5 : Update the display (seconds) every two minutes
UseWiFiServices = 1 #                                       Integer 0 or 1, Indicates is WiFi services should be used

AppName = "MTDL"  #                                         Application name string - Shown at top of display
MsgVerStr = "0.1"  #                                        Version displayed and reported by the software
GUIDStr = "00" #                                            A unique ID string for this board - digits 0 to 9

# Initialise default constants
Graph_Scroll_N = 0 #                                        When Graph_Mode checks and finds this it will over write
Graph_Scroll_L = 1 #                                        When Graph_Mode checks and finds this it will scroll to the left
Graph_Scroll_R = 2 #                                        When Graph_Mode checks and finds this it will scroll to the right
GR_L = 145 #                                                Graph area left start position in pixels
GR_T = 30 #                                                 Graph area top start position in pixels

# Deep Sleep Memory RAM Locations
DSM_Dt_Lg_S_Cnt = 4 #                                       Holds how many sample periods have elapsed - See Data_Lg_S_Cnt
DSM_cnt = 5 #                                               Location for current buffer position / counter
DSM_mx = 6 #                                                Max temperature (with +40 offset)
DSM_mn = 7 #                                                Min temperature (with +40 offset)
DSM_dts = 8 #                                               Date Time Status of last poll of (pseudo) time server
DSM_cts = 9 #                                               Number of time counts before a poll of the (pseudo) time server is made
S_Mem_Offset = 10 #                                         Sleep memory Buffer start offset from zero

Max_Samples = 144 #                                         Long term sample buffer size for graph, nominally 1 day @ 1 sample per 10 minutes
BF_OSV = 50 #                                               Buffer Value Offset for data stored in buffer to obviate negative numbers handling - positive value
BF_max_val = 60 #                                           Maximum value to store in Log buffer
BF_min_val = (-1 * BF_OSV) #                                Minimum value to store in Log buffer

# General Display
Graph_Mode = Graph_Scroll_R #                               See Graph_Scroll constants for behaviours
Segment_Shadow = 1 #                                        Integer 0 or 1 indicating if Segment shadows are shown

ICO_Path = "/ico/" #                                        Icon locations

# Initialise variables
yfi = 0 #                                                   Is WiFi available
mqt = 0 #                                                   Did MQQT complete
cbv = 0 #                                                   Current battery voltage

#---------------------------------------
# Read temperature sensor located in the accelerometer LIS3DH I.C.
# Do this soon after booting to reduce influence of potential board or other thermals
# A MagTag connected to USB may result in a heated PCB and heated LIS3DH I.C.
# The temperature appears to have an offset between different units
# See Calibration notes and settings.toml for compensation
def rd_accel_tmp():
    # set up accelerometer to get temperature
    i2c = board.I2C()  # uses board.SCL and board.SDA
    lis = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)

    #lis._write_register_byte(0x20, 0x20) #                 low power mode with ODR = 10Hz - XYZ Accel. Off
    #lis._write_register_byte(0x24, 0x80) #                 CTRL_REG5

    lis._write_register_byte(0x23, 0x80)  #                 FS = ±2g low power mode with BDU bit enabled
    lis._write_register_byte(0x1F, 0xC0)  #                 Internal Temperature and ADC Enable

    # Get temperature from ADC - Make 2 readings, as 1st read appears to be noise
    dl = (lis._read_register_byte(0x0c)) #                  Low
    dh = (lis._read_register_byte(0x0d)) #                  High

    dl = (lis._read_register_byte(0x0c)) #                  Low
    dh = (lis._read_register_byte(0x0d)) #                  High
    # print ("raw rdg" + str (dh) + " " + str(dl)) #        Debug value obtained
    return tc_to_nm(dh, dl) # return the temperature from the converted register values
#-------------------

#---------------------------------------
# Convert 2's complement to number from two bytes dh and dl
def tc_to_nm(dh, dl):
    nb = dh #                                               For this usage data only in dh, drop dl
    if (nb & 0x80) == 0: #                                  Is MSB set - if not, no conversion
       # Positive
       pass
    else:
       nb = ~(nb - 0xFF) * (-1) #                           MSB was set, convert
    return nb
#-------------------

#---------------------------------------
# Read a value from the buffer and apply (Scaling, Limits, Offsets and Transfer Function as needed)
# Externally, buffer is assumed to be from 0 to maximum and location identified as i
# This function adjusts the actual location as needed via Sleep Memory Offset S_Mem_Offset
# The buffer is used for display graphing so its resolution is purposefully limited to match the display
# This buffer assumes single byte values
def rd_buf(i):
    return (alarm.sleep_memory[i + S_Mem_Offset] - BF_OSV)
#-------------------

#---------------------------------------
# Write a value to the buffer and apply (Scaling, Limits, Offsets and Transfer Function as needed)
# Externally, buffer locations are assumed to be from 0 to maximum and location identified as i
# This function adjusts the actual location as needed via Sleep Memory Offset S_Mem_Offset 'constant'
# The buffer is used for display graphing so its resolution is purposefully limited to match the display
# This buffer assumes single byte values
def wr_buf(i, nmber):
    alarm.sleep_memory[i + S_Mem_Offset] = nmber + BF_OSV
    return
#-------------------

#---------------------------------------
# Obtain environment parameter from settings.toml
# Simplifies management of multiple units and basic settings
# requires CircuitPython 8.0.0 and above for settings.toml file use through os.getenv()
# Set nameStr as the name of the item in setings.toml
# Set min max to be the same for strings, otherwise limits for numeric settings
# Set defStr as the default value to use where no entry or issue identified
# requires access to os library
def get_ev(nameStr, minv, maxv, defStr):
    try:
        x = os.getenv(nameStr) #                            Release 8.0.0 and above
        if (float(minv) < float(maxv)): #                   For numeric values check if min max are different
            if (float(x) <float(maxv)) and (float(x) > float(minv)):
                return x #                                  Numeric value within range - return value read in
            else:
                return defStr #                             Value outside permitted range - return default value
        else:
            return x #                                      No min max checking - return value located
    except:
        return defStr #                                     Issue detected - return default value
#-------------------

#---------------------------------------
# linearise
def linearise(num):
    # In this case apply a simplified y = mx + c to the data
    # accesses settings.toml through get_ev()
    # The default correction factors should be overridden in settings.toml
    # Alternate fit algorithm could be applied here
    # returns an integer
    m0 =  0.9826 #                                          Default correction factor for LIS3DH I.C. in Deg.C i.e. m
    c0 =  26.431 #                                          Default correction factor for LIS3DH I.C. in Deg.C i.e. c
    m0 = get_ev("m0", -30, 30, m0) #                        Get user set Temperature cal. value if available
    c0 = get_ev("c0", -30, 30, c0) #                        Get user set Temperature cal. value if available
    linerise = float(float(m0) * float(num)) + float(c0)
    return int(round(linerise,0)) # Don't overstate the accuracy or precision
#-------------------

#---------------------------------------
# Connect to WiFi using parameters in secrets.py
def wifi_connect():
    # Attempt to connect to the WiFi defined in secrets.py
    # Specific connection related settings e.g. fixed ip address are stored in settings.toml
    # A value indicating status of the whole process is returned 0=issue, 1=success
    wifi_conn = 0
    ipv4_address = get_ev("ipv4_address", 0, 0, "") #       Double check your settings - No checking is done on these
    ipv4_subnet = get_ev("ipv4_subnet", 0, 0, "")
    ipv4_gateway = get_ev("ipv4_gateway", 0, 0, "")
    ipv4_dns = get_ev("ipv4_dns", 0, 0, "")
    try:
        if (ipv4_address > "") and (ipv4_subnet > ""): #    Pre-assigned ip addresses
            wifi.radio.set_ipv4_address(ipv4=ipaddress.IPv4Address(ipv4_address), netmask=ipaddress.IPv4Address(ipv4_subnet), gateway=ipaddress.IPv4Address(ipv4_gateway), ipv4_dns=ipaddress.IPv4Address(ipv4_dns))
        wifi.radio.enabled = True #                         wifi.radio has sole instance
        wifi.radio.connect(secrets["ssid"], secrets["password"])
        wifi_conn = 1
    except:
        wifi_conn = 0
    return wifi_conn #                                       Return the status of connecting to the WiFi
#-------------------

#---------------------------------------
# Publish data to MQQT destination
def publish_to_mqqt(num, cbv, GUIDStr):
    # needs accessed / open WiFi named wifi via import wifi
    # Setup a feed for publishing
    # Inputs published:
    #   num the value being logged
    #   cbv the current battery voltage
    #   note the sample point time is assumed as the publishing time
    # Access secrets.py
    # Uses settings.toml for unique device id via GUIDStr
    mqqt_status = 0
    # print ("MQQT Connection attempt " + str(wifi.radio.enabled))
    try:
        unameStr = secrets["aio_username"] #                    Read once
        mtdl_fd_tmp = unameStr + "/feeds/mtdl-tmp-" + GUIDStr # Associate username and feed name for temperature
        mtdl_fd_cbv = unameStr + "/feeds/mtdl-cbv-" + GUIDStr # Associate username and feed name for battery voltage
        # Create a socket pool for the mqqt client
        pool = socketpool.SocketPool(wifi.radio) #              wifi.radio has sole instance
        # Set up a MiniMQTT Client with parameters needed
        mqtt_client = MQTT.MQTT(
            broker = secrets["broker"],
            port = secrets["port"],
            username = unameStr,
            password = secrets["aio_key"],
            socket_pool = pool,
            ssl_context=ssl.create_default_context()
        )
        # Connect the client to the MQTT broker.
        mqtt_client.connect()
        mqtt_client.publish(mtdl_fd_tmp, num) #                 Publish logged value
        mqtt_client.publish(mtdl_fd_cbv, cbv) #                 Publish Current Battery Voltage
        mqtt_client.loop(2) #                                   Allow send queue processing - 2s normally long enough
        mqqt_status = 1 #                                       MQQT was established - set status
        # print ("MQQT Connection attempt - Complete")
    except:
        mqqt_status = 0
        # print ("MQQT Connection attempt - Issue")
    return mqqt_status
#-------------------

#---------------------------------------
# See is time sync should occur
def sync_time(TimeServiceStatus, TimeServiceCount, TimeSreviceReqCounts, magtag):
    # Using a locale defined in secrets.py sync the local RTC to the Adafruit time service
    # TimeSeviceStatus is used to indicate if the service was successful
    # TimeServiceStatus is preserved if a TimeSerivce sync event is not actioned
    # TimeServiceCount is decremented on every call and reset if time service sync is attempted
    # Only when a time service sync is attempted TimeServiceCount reset to TimeSreviceReqCounts
    if (TimeServiceCount > 0):
        TimeServiceCount -= 1 #                             Decrement the counter on every call
    else:
        TimeServiceCount = TimeSreviceReqCounts #           catch eny errors for the first value

    if (TimeServiceCount == 0): #                           When the count is zero perform a time service update
        try:
            TimeServiceStatus = 0
            magtag.get_local_time() #                       Sync local clock with Adafruit io time sys using loc. set in secrets.py - needs WiFi
            # print ("Time Service Acquired")
            TimeServiceStatus = 1 #                         Only set time service status good if it worked
            TimeServiceCount = TimeSreviceReqCounts #       Reset the counter
        except:
            pass
    return TimeServiceStatus, TimeServiceCount #            Note Tuple returned
#-------------------

# -------><--------><--------><--------><--------><--------><--------><-------->
# Main code
num = rd_accel_tmp() #                                      Get temperature ready for later processing
# print ("Raw data - num " + str(num) ) #                   Debug output
num = linearise(num)  #                                     Apply Calibration factors to previously read raw value

magtag = MagTag() #                                         Access to the MagTag Object
cbv = magtag.peripherals.battery  #                         Read Current Battery Voltage as soon as reasonable

# Over ride internal settings with settings from settings.toml
GUIDStr = get_ev("GUIDStr", 0, 0, "00") #                   A unique ID string for this board - digits 0 to 9
Segment_Shadow = get_ev("Segment_Shadow", 0, 1, 0) #        Users segment shadow preference
Dis_Upd_Prd = int(get_ev("Sample_Period", 0, 600, Dis_Upd_Prd)) #   Sample rate for display update default is 120
UseWiFiServices = get_ev("UseWiFiServices", 0, 1, 1) #      Are WiFi services to be used

wdt = microcontroller.watchdog #                            Establish watchdog to allow recovery and prevent battery exhaustion
wdt.timeout = 60 #                                          Watchdog timeout - will allow recovery from unanticipated issues e.g. WiFi

#---------------------------------------
# Actions taken if not an alarm wake up e.g on manual reset
# print (AppName + " - Wake cause " + str(alarm.wake_alarm)) # debug output of wake cause
if not alarm.wake_alarm: #                                  Allow wipe of legacy data
    PonText = magtag.add_text( #                            Power On Text for probable manual reset
        text_position=( #                                   Name - Top of Screen
            0, #                                            X position
            64, #                                           Y position
        ),
        text_font = "/fonts/Arial-Bold-12.bdf",
        text_color = 0x000000, #                            Deepest darkest black font
        text_wrap = 20, #                                   Auto text wrapping
        #       123456789012345678901234567890123456789012345678901234567890
        text = " MagTag Data Logger  Erase previous log?  Yes  (3s timeout) ", # With default text will auto display
        text_scale = 1, #                                   1 = small
    )
    if (hlp.pause_or_press(magtag, 6) == 1): #              User selected yes button
        # Initialise deep sleep RAM values if needed
        # print (AppName + " - Reset Request") #            Debug output - User selection activated
        alarm.sleep_memory[DSM_cnt] = 0 #                   Logger memory position count
        alarm.sleep_memory[DSM_mx] = 0 #                    Maximum logged value
        alarm.sleep_memory[DSM_mn] = 99 #                   Minimum logged value
        alarm.sleep_memory[DSM_dts] = 0 #                   Date Time Status of synchronisation (updated at logger frequency)
        for i in range(0, Max_Samples -1): #                Only clear buffer if user requested
            # wr_buf(i, 20 ) #                              Simulate buffer full for testing
            wr_buf(i, (-1 * BF_OSV))  #                     Initialise buffer with minimum possible values

    magtag.remove_all_text() #                              (Secret magic) method to remove text setups ;-)

    # Establish time sync on new or requested reset
    if (UseWiFiServices == 1): #                            Are WiFi services to be accessed
        yfi = wifi_connect() #                              Attempt to establish a WiFi connection using params in secrets.py
        # print ("yfi status " + str(yfi))
        if (yfi == 1): #                                    Was a WiFi connection established
            # Froce initialise the Time Service Request counter and time sync
            TS_Tuple = sync_time(alarm.sleep_memory[DSM_dts], alarm.sleep_memory[DSM_cts], 1, magtag ) #  Synchronise the internal clock
            alarm.sleep_memory[DSM_dts] = int(TS_Tuple[0]) # Update date time service status for later indication
            alarm.sleep_memory[DSM_cts] = int(get_ev("TimeServiceReqCounts", 1, 20, 1)) # intialise counter or set default
            TS_Tuple =  "" #                                We don't need this again
            TS_Req_Cnts = ""
#-------------------

#---------------------------------------
# MQQT support
yfi = 0 #                                                   Clear WiFi status, will be used to set icon status
mqt = 0 #                                                   Clear MQQT status, will be used to set icon status
if (UseWiFiServices == 1): #                                Are WiFi services to be accessed
    yfi = wifi_connect() #                                  Attempt to establish a WiFi connection using params in secrets.py
    # print ("yfi status " + str(yfi))
    if (yfi == 1): #                                        Was a WiFi connection established
        mqt = publish_to_mqqt(num, cbv, GUIDStr) #          Push data & current battery voltage to MQQT recipient server
        # print ("MQQT Status " + str(mqt))
        TS_Req_Cnts = int(get_ev("TimeServiceReqCounts", 1, 20, 1)) # Get the default number of counts
        TS_Tuple = sync_time(alarm.sleep_memory[DSM_dts], alarm.sleep_memory[DSM_cts], TS_Req_Cnts, magtag ) #  Synchronise the internal clock
        alarm.sleep_memory[DSM_dts] = int(TS_Tuple[0])
        alarm.sleep_memory[DSM_cts] = int(TS_Tuple[1])
        wifi.radio.enabled = False #                        Power down WiFi - if MQQT does not complete increase MQQT loop time
        TS_Tuple =  "" #                                    We don't need this again
        TS_Req_Cnts = ""
#-------------------

#---------------------------------------
# Process data
if (num < BF_min_val): #                                    Sanity check the acquired date value and limit if necessary
    num = BF_min_val #                                      Note (-1 * BF_OSV) is the minimum real value that could be stored
elif (num > BF_max_val):
    num = BF_max_val #

cnt = alarm.sleep_memory[DSM_cnt] #                         Get current buffer location / count from Deep Sleep Memory
alarm.sleep_memory[DSM_Dt_Lg_S_Cnt] += 1 #                  Increment the wake ups until data is logged count in Deep Sleep Memory
# print (AppName + " " + str(alarm.sleep_memory[DSM_Dt_Lg_S_Cnt])) # Debug output
if (alarm.sleep_memory[DSM_Dt_Lg_S_Cnt] >= Data_Lg_S_Cnt): # Do we need to update the Log buffer
    alarm.sleep_memory[DSM_Dt_Lg_S_Cnt] = 0 #               Reset the Data Log Sample Counter
    alarm.sleep_memory[DSM_cnt] = (alarm.sleep_memory[DSM_cnt] + 1) % (Max_Samples -1) # Increment the current count / buffer location

    if (Graph_Mode == Graph_Scroll_N):
        wr_buf(cnt, num) #                                  # Wrap around - Store the current data in the buffer
    elif (Graph_Mode == Graph_Scroll_L):
        for i in range(Max_Samples - 1, 0, -1):
            wr_buf(i, rd_buf(i - 1)) #                      Move samples up one place - Scroll data to L with old data falling off the right
        wr_buf(0, num) #                                    Store the current data in the buffer Left most
    elif (Graph_Mode == Graph_Scroll_R):
        for i in range(0, Max_Samples - 1, 1):
            wr_buf(i, rd_buf(i + 1)) #                      Move samples down one place - Scroll data to R with old data falling off the left
        wr_buf(Max_Samples - 1, num) #                      Store the current data in the buffer Right most
    else:
        # We did not fill the buffer yet
        wr_buf(cnt, num) #                                  Store the current data in the buffer
#-------------------

#---------------------------------------
# Update min max values held in Deep Sleep memory and for later display
if num > (alarm.sleep_memory[DSM_mx] - BF_OSV):
    alarm.sleep_memory[DSM_mx] = num + BF_OSV #             Store the new maximum (with Buffer Offset Value applied)
if num < (alarm.sleep_memory[DSM_mn] - BF_OSV):
    alarm.sleep_memory[DSM_mn] = num + BF_OSV #             Store the new minimum (with Buffer Offset Value applied)
#-------------------

#---------------------------------------
# Graph mode - Over write or Scroll - Moving the buffer - Possibly better with head, tail and direction
if (cnt == Max_Samples):
    if (Graph_Mode == Graph_Scroll_N):
        pass #                                              Wrap around
    elif (Graph_Mode == Graph_Scroll_L):
        for i in range(0, Max_Samples - 1):
            wr_buf(i, rd_buf(i + 1)) #                      Move samples up one place - Scroll from R to L
    elif (Graph_Mode == Graph_Scroll_L):
        for i in range(1 , Max_Samples - 1):
            wr_buf(i, rd_buf(i - 1)) #                      Move samples down one place - Scroll from L to R
#-------------------

#---------------------------------------
# Icon display setup
hlp.load_vlt_icon(hlp.Current_Battery_Level(cbv), magtag) #           Rank Current Battery Level for this run, Show battery level icon
if hlp.USB_Connected():
    hlp.load_small_icon("16x16-usbicon01.bmp", 2, magtag) #           USB Icon - On - Connected
else:
    hlp.load_small_icon("16x16-usbicon02.bmp", 2, magtag) #           USB Icon - Off - Disconnect

if (yfi == 1): #                                                      Assessed WiFi OK
    hlp.load_small_icon("16x16-routicon01.bmp", 42, magtag) #         WiFi router
    # Potential to use actual rssi - takes time and power - simplified
    hlp.load_wif_icon(80, magtag)  #                                  Display a WiFi Icon
else:
    hlp.load_small_icon("16x16-routicon00.bmp", 42, magtag) #         No WiFi router
    hlp.load_wif_icon(1, magtag)  #                                   Display a WiFi Icon

if (mqt == 1): #                                                      Assessed MQQT was good
    hlp.load_small_icon("16x16-glb01icon.bmp", 22, magtag) #          Globe - Functional MQQT Internet connection
else:
    hlp.load_small_icon("16x16-glb00icon.bmp", 22, magtag) #          Globe - Exclamation - Bad MQQT Internet connection

if (alarm.sleep_memory[DSM_dts] == 1): #                              What was the last date time poll status
    hlp.load_small_icon("16x16-cal-ok.bmp", 64, magtag) #             Calendar OK icon for date time good sync
else:
    hlp.load_small_icon("16x16-cal-error.bmp", 64, magtag) #          Calender Exclamation icon for bad date time sync
#-------------------

#---------------------------------------
# Data Presentation
#---------------------------------------
magtag.add_text( #
    text_position=( #                                       Name - Top of Screen
        120, #                                              X position
        6, #                                                Y position
    ),
    text_font = "/fonts/Arial-Bold-12.bdf",
    text_color = 0x000000,
    # text="MagTag", #                                      Default Text
    text_scale=1 #                                          1 = small
)

magtag.add_text( #                                          Place holder large temperature segment display - Active segments
    text_position=( #
        110, #                                              X position
        96, #                                               Y position
    ),
    text_font = "/fonts/DSEG14Classic-Regular-64.bdf", #    Source - see bdf file
    text_maxlen = 3, #                                      Only 2 digits long
    text_color = 0x000000, #                                Black
    text_anchor_point = (1.0,1.0), #                        Anchor text at bottom right for right justified
    # text="00", #                                          Default text
    text_scale=1 #                                          1 = small
)

if (Segment_Shadow == 1):
    magtag.add_text( #                                      Place holder large temperature segment display - Shadow segments
        text_position=( #
            110, #                                          X position
            96, #                                           Y position
        ),
        text_font = "/fonts/DSEG14Classic-Regular-64.bdf", #  Source - see bdf file
        text_maxlen = 2, #                                  Only 2 digits long
        text_color = 0x999999, #                            Set colour for shadow
        text_anchor_point = (1.0,1.0), #                    Anchor text at bottom right for right justified
        # text="~~", #                                      Default text ~~ is all segments on
        text_scale=1  #                                     1 = small
    )
else:
    magtag.add_text( #                                      Place holder large temperature segment display - Shadow segments
        text_position=( #
            110, #                                          X position
            96, #                                           Y position
        ),
        text_font = "/fonts/DSEG14Classic-Regular-64.bdf", #  Source - see bdf file
        text_maxlen = 2, #                                  Only 2 digits long
        text_color = 0xFFFFFF, #                            Set colour for shadow
        text_anchor_point = (1.0,1.0), #                    Anchor text at bottom right for right justified
        # text="~~", #                                      Default text ~~ is all segments on
        text_scale=1 #                                      1 = small
    )

magtag.add_text( #                                          Place holder Degrees
    text_position=( #
        110, #                                              X position
        32, #                                               Y position
    ),
    text_font = "/fonts/Arial-Italic-12.bdf",
    text_color = 0x000000,
    text_scale = 2 #                                        1 = small
)

magtag.add_text( #                                          Place holder Units
    text_position=( #
        113, #                                              X position
        87, #                                               Y position
    ),
    text_font = "/fonts/Arial-Italic-12.bdf",
    text_color = 0x000000,
    text_scale = 1 #                                        1 = small
)

magtag.add_text( #                                          Status bar text format
    text_position=( #                                       Bottom of screen
        30, #                                               X position
        121, #                                              Y position
    ),
    text_color = 0x000000,
    text_scale = 1 #                                        1 = small
)

magtag.add_text( #                                          Time Of Last Update Text
    text_position=( #                                       Bottom of screen
        200, #                                              X position
        106, #                                              Y position
    ),
    text_color = 0x000000,
    text_scale = 1 #                                        1 = small
)
#                         Xl, Yt, Xr, Yb
magtag.splash.append(Line(0, 17 ,295, 17,  0x000000)) #     Draw division line for ICON bar at top of display

magtag.splash.append(Line(0, 114 ,295, 114,  0x000000)) #   Draw division line for Status bar at bottom of display

#---------------------------------------
# Draw Graph elements
magtag.splash.append(Line( GR_L, GR_T, GR_L, GR_T + 70,  0x000000))
magtag.splash.append(Line( GR_L + Max_Samples +1, GR_T, GR_L + Max_Samples + 1, GR_T + 70,  0x000000))

# Y axis ticks
for i in range (0, 71, 10):
    # Left Chart Ticks
    magtag.splash.append(Line( GR_L - 3, GR_T + 70 - i, GR_L, GR_T + 70 - i,  0x000000))
    # Right Chart Ticks
    magtag.splash.append(Line( GR_L + Max_Samples +1, GR_T + 70 -i, GR_L + Max_Samples + 4, GR_T + 70 -i,  0x000000))

#---------------------------------------
#Plot data to graph with reference to 0 C line
for i in range(0, Max_Samples):
    if (rd_buf(i) > (-1 * BF_OSV)): # Is the buffer value greater than the lowest value held in the buffer
        # Light colour fill below data - If no fill desired, comment out this line
        magtag.splash.append(Line(i + GR_L +1, (GR_T + 50), i + GR_L + 1, (GR_T + 50) - rd_buf(i),  0x999999)) # Light Fill line graph
        # Dark data point
        magtag.splash.append(Line(i + GR_L +1, (GR_T + 50)  - rd_buf(i), i + GR_L + 1, (GR_T + 50) - rd_buf(i),  0x000000)) # Point


# create graph graticule
for i in range(0, Max_Samples, 6): #                        X Axis increments
    for j in range(0, 71, 10): #                            Y Axis increments
        magtag.splash.append(Line(i + GR_L +1, (GR_T + j), i + GR_L + 1, (GR_T + j),  0x666666)) # Point

# create graticule zero
for i in range(0, Max_Samples, 6): #                        X Axis increments
    magtag.splash.append(Line(i + GR_L +1, (GR_T + 50), i + GR_L + 1, (GR_T + 50),  0x000000)) # Point
    magtag.splash.append(Line(i + GR_L +2, (GR_T + 50), i + GR_L + 2, (GR_T + 50),  0x000000)) # Point
#-------------------

#---------------------------------------
# Update previously set text elements of the display
if (num >-40): # In Deg C - Not to cold for the display - Testing showed issues ~ -18 C
    magtag.set_text("MTDL", 0, False) #                     App title
    magtag.set_text("~~", 2, False) #                       Shadow of display
    magtag.set_text(str(num), 1, False) #                   Data value
    magtag.set_text("°", 3, False) #                        Degrees symbol
    magtag.set_text("C", 4, False) #                        Units
    magtag.set_text(str(num) + " C  Max=" + str(alarm.sleep_memory[DSM_mx] - BF_OSV) + "  Min=" + str(alarm.sleep_memory[DSM_mn] - BF_OSV) + "  Cnt=" + str(cnt) + "  Bat=" + "{:.1f}".format(cbv) + " V", 5, False)
    magtag.set_text(str(hlp.hh_mm(time.localtime(),False)), 6, False)
    magtag.refresh() #                                      Draw all text & graph changes to the display
#-------------------

#---------------------------------------
# Calculate when to wake - with external time sync available this means sampling aligns with minute intervals
# As network operations can have variable length we need to compensate for next wake up point
# - Possibly not practicable for less than 30s sleep intervals
SLP_Offset = Dis_Upd_Prd - (time.time() % Dis_Upd_Prd) #    Arrange to wake up at the next interval boundary point
print ("Sleep Offset " + str(SLP_Offset))
# Set the point at which the sleep period should wake us up for the next sample
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + SLP_Offset)

wdt.deinit() #                                              Turn off the watchdog

# Enter Deep Sleep until the next sample point
alarm.exit_and_deep_sleep_until_alarms(time_alarm)


# --------------------------------------
#
# --------------------------------------
# End of code
# --------------------------------------
"""
# --------------------------------------
#
# --------------------------------------
2023-02-25 -
             Align sampling to minute boundaries
             WiFi and logging routine tidy
             Linearise routine now self contained
             Comment updates
             Source location comment updated from MTMP to MTDL


2023-02-20 -
             Added place holders to settings.toml for web based workflow at
             http://circuitpython.local/code/
             For setup see:
             https://learn.adafruit.com/circuitpython-with-esp32-quick-start/setting-up-web-workflow
             https://learn.adafruit.com/getting-started-with-web-workflow-using-the-code-editor/device-setup

2023-02-19 -
             Support for pre-assigned IP address in settings.toml for speed & power reduction

2023-02-18 -
             Added USB detection and indication on Tool bar
             Additional code comments
             Reduce debug code printing
             Added wifi.radio.enabled(false) to reduce power consumption

2023-02-16 -
             Unsupported Beta release
             No further back testing will be performed on pre CircuitPython 8.x.x comments amended
             Applied round to improve linearise function also prepares for future averaging or over sampling
             Removed some print to console items used during development
             Added UseWiFiServices switch to permit lower power consumption

2023-02-07 -
             Added wipe log history prompt on non deep sleep wake_alarm
             Added publish cbv (Current Battery Voltage to MQQT feed to allow remote battery monitoring
             Added watchdog to handle errant WiFi or other network related issues - Code of last resort
             REPL messages now use AppName to assist identifying App reporting out to REPL

2023-02-05 -
             Added MQQT
             Modified for independent display and log updates
             Adjusted segment display for right justification

2023-02-03 - Font Conversion
             https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display/conversion
             Font credit - https://www.keshikan.net/fonts.html - Open Font License applies

2023-01-30 - 0.1 - Development Starts
# --------------------------------------
"""
