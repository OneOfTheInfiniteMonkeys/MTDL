# MTDL (MagTag Data Logger) - {Pre-Release}
MagTag Data Logger is a CircuitPython data logger that permits ambient temperature monitoring in the environment of the device using an internal sensor on the MagTags PCB (other data could readily be logged). With minimal calibration, obviates the need for additional external hardware. Typically 1 C resolution, ±1 C accuracy, ~0.35 C / minute for a 5 C step change, range -20 to +60 C. Based on Adafruit example code, additional features include Segment numeric indicator and Data graphing on the e-ink display of the <a target="_blank" rel="noopener noreferrer" href="https://www.adafruit.com/product/4800">Adafruit</a> <a target="_blank" rel="noopener noreferrer" href="https://cdn-learn.adafruit.com/downloads/pdf/adafruit-magtag.pdf"> Magtag</a> device.

<div align="center">
  <div style="display: flex; align-items: flex-start;">
  <img src="https://raw.githubusercontent.com/OneOfTheInfiniteMonkeys/MTDL/main/images/20230205-MTDL-Beta.jpg?raw=true" width="400px" alt="Adafruit Magtag Data Logger PCB. Image copyright (c) 05 Feb 2023 OneOfTheInfiniteMonkeys All Rights Reserved">
  </div>
</div>  

[![Language](https://img.shields.io/static/v1?label=CircuitPython&message=9.0.0&color=blueviolet&style=flat-square)](https://circuitpython.org/board/adafruit_magtag_2.9_grayscale/)
[![MagTag](https://img.shields.io/badge/gadget-MagTag-blueviolet.svg?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgdmlld0JveD0iMTIgMTIgNDAgNDAiPjxwYXRoIGZpbGw9IiMzMzMzMzMiIGQ9Ik0zMiwxMy40Yy0xMC41LDAtMTksOC41LTE5LDE5YzAsOC40LDUuNSwxNS41LDEzLDE4YzEsMC4yLDEuMy0wLjQsMS4zLTAuOWMwLTAuNSwwLTEuNywwLTMuMiBjLTUuMywxLjEtNi40LTIuNi02LjQtMi42QzIwLDQxLjYsMTguOCw0MSwxOC44LDQxYy0xLjctMS4yLDAuMS0xLjEsMC4xLTEuMWMxLjksMC4xLDIuOSwyLDIuOSwyYzEuNywyLjksNC41LDIuMSw1LjUsMS42IGMwLjItMS4yLDAuNy0yLjEsMS4yLTIuNmMtNC4yLTAuNS04LjctMi4xLTguNy05LjRjMC0yLjEsMC43LTMuNywyLTUuMWMtMC4yLTAuNS0wLjgtMi40LDAuMi01YzAsMCwxLjYtMC41LDUuMiwyIGMxLjUtMC40LDMuMS0wLjcsNC44LTAuN2MxLjYsMCwzLjMsMC4yLDQuNywwLjdjMy42LTIuNCw1LjItMiw1LjItMmMxLDIuNiwwLjQsNC42LDAuMiw1YzEuMiwxLjMsMiwzLDIsNS4xYzAsNy4zLTQuNSw4LjktOC43LDkuNCBjMC43LDAuNiwxLjMsMS43LDEuMywzLjVjMCwyLjYsMCw0LjYsMCw1LjJjMCwwLjUsMC40LDEuMSwxLjMsMC45YzcuNS0yLjYsMTMtOS43LDEzLTE4LjFDNTEsMjEuOSw0Mi41LDEzLjQsMzIsMTMuNHoiLz48L3N2Zz4%3D&style=flat-square)](https://github.com/adafruit/Adafruit_MagTag_PCBs)
![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/OneOfTheInfiniteMonkeys/MTDL?&include_prereleases&style=flat-square)
[![GitHub License](https://img.shields.io/github/license/OneOfTheInfiniteMonkeys/MTDL?style=flat-square)](https://github.com/OneOfTheInfiniteMonkeys/MTMP/blob/main/LICENSE) 
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=flat-square)](https://github.com/OneOfTheInfiniteMonkeys/mtdl/graphs/commit-activity)
![GitHub repo size](https://img.shields.io/github/repo-size/OneOfTheInfiniteMonkeys/MTDL?style=flat-square)

## Introduction
The <a rel="noopener noreferrer" href="https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython" target="_blank">CircuitPython</a> implementation of the MagTag Data Logger is intended to allow ambient e.g. room temperature monitoring without need for additional sensing hardware. The software permits logging and on board graphing of the measured temperature. For accurate measurements a reference temperature point should be established, perhaps with reference to an existing room sensor (see Calibration section) and this operation should only be required once. Where relative temperatures are satisfactory, no calibration is necessary. Other data from a variety of sources could be logged with relatively minor modification. General information on CircuitPython data loggers can be found <a rel="noopener noreferrer" href="https://learn.adafruit.com/a-logger-for-circuitpython/overview" target="_blank">here</a>.

## Installation
Requirements
- <a rel="noopener noreferrer" href="https://www.adafruit.com/product/4800" target="_blank">Adafruit Magtag</a>
- <a rel="noopener noreferrer" href="https://www.adafruit.com/product/4236" target="_blank">Adafruit LiPo Cell (typical)</a>
- <a rel="noopener noreferrer" href="https://downloads.circuitpython.org/bin/adafruit_magtag_2.9_grayscale/en_GB/adafruit-circuitpython-adafruit_magtag_2.9_grayscale-en_GB-9.0.0.uf2" target="_blank">CicruitPython 9.0.0</a>

Optional  
- <a rel="noopener noreferrer" href="https://en.wikipedia.org/wiki/USB-C" target="_blank">USB C cable connection to host computer</a>

Download and unzip the <a href="https://github.com/OneOfTheInfiniteMonkeys/MTDL/zipball/master/">Repository Zip file</a>.  
Make sure you are using the correct versio of CircuitPython for the release.  
Then copy the files located in the 'dist' folder of the unzipped files to the CIRCUITPY drive (root) folder of the Adafruit MagTag.  

There are two setup files:  
<table>
  <tr><th>File</th><th>Comment</th></tr>
  <tr><td><a rel="noopener noreferrer" href="https://github.com/OneOfTheInfiniteMonkeys/MTDL/blob/main/dist/secrets.py" target="_blank">secrets.py</a></td><td>WiFi and other account specific settings</td></tr>
  <tr><td><a rel="noopener noreferrer" href="https://github.com/OneOfTheInfiniteMonkeys/MTDL/blob/main/dist/settings.toml" target="_blank">settings.toml</a></td><td>Unit specific settings i.e. Calibration, identifiers, options</td></tr>
</table>

Use of settings.toml is covered below and the comments in the file, details on secrets.py are in the link <a rel="noopener noreferrer" href="https://learn.adafruit.com/electronic-history-of-the-day-with-pyportal/code-walkthrough-secrets-py" target="_blank">here</a>.  
WiFi or other settings in secrets.py are not required to use the logger, some features can not be used without WiFi access.

Note 
- The implementation may optionally use WiFi and thus a secrets.py file should typically have any entries, it must be in the CIRCUITPY drive .
- Following release of <a rel="noopener noreferrer" href="https://github.com/adafruit/circuitpython/releases" target="_blank">CircuitPython 7</a> to stable, the code implements switch off of HID disk and serial ports via <a rel="noopener noreferrer" href="https://github.com/OneOfTheInfiniteMonkeys/MTDL/blob/main/dist/boot.py" target="_blank">boot.py</a>.
- If electing to use alternate CircuitPython releases <a rel="noopener noreferrer" href="https://github.com/adafruit/circuitpython/releases" target="_blank"> e.g. CircuitPython 7.1.x etc.</a> you need to replace the lib .mpy files with the release counterparts in the lib folder.
- The '<a rel="noopener noreferrer" href="https://github.com/OneOfTheInfiniteMonkeys/MTDL/blob/main/Magtag%20PowerPoint%20Layout%2003.pptx" target="_blank">Magtag PowerPoint Layout 03.pptx</a>' file is a Microsoft&trade; PowerPoint&trade; pack with slidemaster backgrounds consisting of a Magtag graphic to enable graphic design prior to coding. The image scale approximates to 2:1 The file should load into Google&trade; Docs, though this has not be tested.
- Ensure any temperature changes result in no condensation in or on the electronics
- LiPo cells may degrade at temperature extremes
- Display may not operate at low temperatures, the software is coded to omit updates below -9 C
- Operation outside the manufacturers specification(s) for any component must not occur

## Hardware
Optional - A <a rel="noopener noreferrer" href="https://www.adafruit.com/product/4236" target="_blank">LiPo</a> battery, supported by the MagTag.  
Suggested - <a rel="noopener noreferrer" href="https://www.adafruit.com/product/4807" target="_blank">Acrylic + Hardware Kit for Adafruit MagTag</a>  

## Discussion
Design of the MagTag means that when the unit is powered from the USB port the on board voltage regulator and ESP32-S2 cause the units PCB to be heated. To approximately 32 C with a room ambient of 22 C under typical continuous use conditions with <a href="https://codewith.mu/" target="_blank">Mu editor</a> (even with <a rel="noopener noreferrer" href="https://docs.circuitpython.org/en/latest/shared-bindings/alarm/index.html" target="_blank">sleep modes</a>). This heating effect (see image below) causes a measurement error and unless the PCB temperature is desired, powering from the USB port typically prevents ambient temperature sensing due to the typical heat soak from the ESP32-S2 and voltage regulators and particularly so when charging a battery as is shown in the thermal image here.  

<div align="center">
  <div style="display: flex; align-items: flex-start;">
  <img src="https://raw.githubusercontent.com/OneOfTheInfiniteMonkeys/MTDL/main/images/MagTag-Thermal-USB-Powered-00.jpg?raw=true" width="400px" alt="Adafruit MagTag Data Logger PCB with USB power, Thermal Image. Image copyright (c) 04 Feb 2023 OneOfTheInfiniteMonkeys All Rights Reserved. Emissivity set for PCB, room ambient 22 C">
  </div>
</div>  

Without a battery, Mu editor and USB services together with arranging a power on duration to be suitably short and a power off duration to be suffciently long. Permit the unit to maintain its self at an ambient temperature. Thus allowing an arrangment for a permenantly powered temperature monitor. Alternatively power can be drawn from a LiPo battery (keeping in mind whilst being charged via the MagTag the PCB warms as shown). It should be noted that when the LiPo has charged the unit does cool. However, the cycle for recharging the LiPo is not <a rel="noopener noreferrer" href="https://learn.adafruit.com/adafruit-magtag?view=all#power-3077160" target="_blank">controllable</a> by software and may confuse interpretation of readings as a result.

Use of magnetic stand off feet to attach the MagTag to a metallic surface will modify the devices temperature responsiveness and thermal heat soak profile. Where not powered from the USB port and the attachment point moves largely with the environment (room) the impact would be anticipated to somewhat limited, if somewhat slower than the air temperature change.  

For sensing of the ambient temperature, air flow over the rear of the MagTag should ideally not be restricted. Testing within a <a rel="noopener noreferrer" href="https://raw.githubusercontent.com/OneOfTheInfiniteMonkeys/MTMP/main/images/MagTag-MacroPad-00.png" target="_blank">plastic</a> case where the MagTag was substantially attached to the housing demonstrated reasonable thermal responsiveness arising from the design decisions, materials and construction.  

## Calibration
To calibrate the device a performance curve was obtained as shown below. Depending on the level of accuracy required various mechanisms might be employed for calibration, such as multi <a rel="noopener noreferrer" href="https://en.wikipedia.org/wiki/Degree_of_a_polynomial" target="_blank">degree (order) polynomials</a> or <a rel="noopener noreferrer" href="https://en.wikipedia.org/wiki/Lookup_table" target="_blank">lookup tables</a>. In the release software it was elected to implement a straightforward compensation based on a straight line y = mx + c. The LIS3DH MEMS digital output motion sensor device specification points to 1 C per bit. Each measurement point of the performane curve was repeated three times. The variation observed might be associated with measurement uncertainty of the characterisation system rather than the device its self. For other MagTag devices it is probably satisfactory to assess the offset at a reference temperature to achieve reasonable performance.  

<div align="center">
  <div style="display: flex; align-items: flex-start;">
  <img src="https://github.com/OneOfTheInfiniteMonkeys/MTDL/blob/main/images/MagTag-Temperature-Reading-Correlation-LIS3DH.png?raw=true" width="400px" Alt="Adafruit MagTag LIS3DH MEMS digital output motion sensor, temperature performance characterisation. Copyright 14 Feb 2023 OneOfTheInfiniteMonkeys All Rights Reserved. Measurement resolution 0.1 C, Room ambient 22 C">
  </div>
</div>

From two randomly selected MagTag devices purchased at the same time, the offset difference was found to be ~6 units.  
  
Calibration is performed by adjusting values in the <a rel="noopener noreferrer" href="https://learn.adafruit.com/scrolling-countdown-timer/create-your-settings-toml-file" target="_blank">settings.toml</a> file stored in the root folder of the CIRCUITPY MagTag device.  
The values m0 and c0 are set to 1.0 and 0.0 respectively in the settings.toml distribution. To cause the display to scale to raw sensor units used in the compensation calculation y = mx + c . Where m is assigned from m0 and c is assigned from c0 via the settings.toml file (default values are applied if no settings exist).  

For basic adjustment, if assuming similar performance to the curve shown:  
  1) Set the value of m0 to 0.9826 from the default of 1.0 in the settings.toml file 
  2) Using a charged battery and no USB connection, with the default display sample period of 120 seconds  
  3) Allow the unit to thermally settle at a fixed reference temperature for one hour  
     (The display should update every 2 minutes, a WiFi connection is not required)  
  4) Edit the value c0 in the settings.toml to offset the reading to the stabilised reference temperature  
     (e.g if the displayed value is 20 C too low, set c0 to 20.0 in the settings.toml file and reboot the device)
  
A more rigorous approach might be to arrange to identify the raw 0 temperature or even perform a custom multi point calibration.  
To perform a custom calibration, set m0 to 1.0 and c0 = 0.0 in the settings.toml file to cause data display in raw values. These can then be read to create a calibration curve similar to that shown for specific temperature(s). A number of approaches can be taken such as multipoint calibration as desired. In the case of the characteristic shown the reference temperature indication had a resolution of 10 times the nominal raw value increments. Care was exercised to maintain as low a temperature gradient across the device as practicable e.g. in a thermally controlled environment.



Note 
The settings.toml file can be accessed by keeping the button D11 next to the USB connector depressed during the boot sequence. The boot sequence is initiated by pressing the reset button once. This will cause the <a rel="noopener noreferrer" targt="_blank" href="https://learn.adafruit.com/circuitpython-essentials/circuitpython-storage" >boot.py</a> file to detect the button press and enable the USB drivers required for serial port <a rel="noopener noreferrer" href="https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop" target="_blank">REPL</a> and <a rel="noopener noreferrer" target="_blank" href="https://learn.adafruit.com/customizing-usb-devices-in-circuitpython" >emulated USB memory device</a> etc.

## Battery Life
The curve below is taken from a unit logging at 120 second intervals from a fully charged 2000 mAh PKCELL LP803860 <a rel="noopener noreferrer" href="https://learn.adafruit.com/products/4236/guides" target="_blank">LiPo</a> battery. The WiFi signal strength was <a rel="noopener noreferrer" targt="_blank" href="https://en.wikipedia.org/wiki/DBm">~-30 dBm</a>, the WiFi Channel has been identified and a maximum 10 seconds permitted for WiFi acquisition in the settings.py file.  
  
<div align="center">
  <div style="display: flex; align-items: flex-start;">
  <img src="https://github.com/OneOfTheInfiniteMonkeys/MTDL/blob/main/images/LoadedDischargeCurve00.png?raw=true" width="400px" alt="Adafruit MagTag 120 second loaded battery performance characterisation. Copyright 15 Feb 2023 OneOfTheInfiniteMonkeys All Rights Reserved.">
  </div>  
</div>  

It should be noted that placing the LiPo battery attached to the rear of the MagTag will affect the thermal inertia. The capacity of the LiPo battery impacts the charge time. LiPo battery warnings are set to 3.7 Volts, ~88% new battery terminal voltage, lower voltages are <a rel="noopener noreferrer" href="https://cdn-shop.adafruit.com/datasheets/785060-2500mAh_specification_sheet.pdf" target="_blank">not recomended</a>. It was found allowing battery terminal voltage to fall lower also resulted in excessive charge times.
  
## Example Data Logging 
The data below was sampled every 120 seconds over a number of days.  
<div align="center">
  <div style="display: flex; align-items: flex-start;">
  <img src="https://github.com/OneOfTheInfiniteMonkeys/MTDL/blob/main/images/MagTag-Temperature-Data-With-Test-Filter-00.png?raw=true" width="400px" alt="Adafruit MagTag 120 second temperature data and test filter. Copyright 03 Mar 2023 OneOfTheInfiniteMonkeys All Rights Reserved.">
  </div>  
</div>  

The raw data is shown with a test data filter (in Orange). The (optional) filter configuration is selected to introduce minimal delay, exhibit good step response to (relatively) rapidly changing temperature data, have straight forward implementation and a response that is a good match for the experienced environment. The test filter has the transfer function y[n] = (0.1 * x[n]) + (0.9 * x[n-1]), these are (will be) settable in the settings.toml file such that the performance can be readily adjusted.  

The graphed data for Battery and Temperature were retreived from the published MQQT data streams (see MQQT below).  

## MQQT
Two <a rel="noopener noreferrer" href="https://en.wikipedia.org/wiki/MQTT" target="_blank">MQQT</a> streams are published if suitable settings are applied to the 'secrets.py' file. The streams are Temperature and Voltage of the battery (or USB if powered from a USB port).  

<div align="center">
  <div style="display: flex; align-items: flex-start;">
  <img src="https://github.com/OneOfTheInfiniteMonkeys/MTDL/blob/main/images/2023-10-20%20Example%20Logged%20Datat.png?raw=true" width="400px" alt="Adafruit IO MQQT MagTag Data Log. Image copyright (c) 20 Oct 2023 OneOfTheInfiniteMonkeys All Rights Reserved.">
  </div>
</div>  

The data taken over a number of days shows that if the 2000 mAh battery terminal voltage drop due to dicharge is kept to less than ~ 0.1 Volt, ~ 8 hours. The subsequent re-charge cycle does not unduly influence measured temperature. Voltage delta might be used to detect removal of the USB power as the MagTag can not identify the power source.

See <a rel="noopener noreferrer" href="https://learn.adafruit.com/mqtt-in-circuitpython" target="_blank">here</a> for more information on MQQT.   

## Features Summary
The key features are shown below:
  
<div align="center">
  <div style="display: flex; align-items: flex-start;">
  <img src="https://github.com/OneOfTheInfiniteMonkeys/MTDL/blob/main/images/MagTag-Data-Logger-Basic-Features-00.png?raw=true" width="960px" alt="Adafruit MagTag Data Logger Basic Features. Copyright 17 Feb 2023 OneOfTheInfiniteMonkeys All Rights Reserved.">
  </div>  
</div>  

## Note
An external temperature (or other) sensor(s) channel could readily be substituted, via the <a rel="noopener noreferrer" href="https://learn.adafruit.com/adafruit-magtag/pinouts#stemma-qt-3077167" alt="Adafruit MagTag Stemma Connector Link">MagTags QWIC StemmaQT</a> data connections if desired.
  
  
DSEG14 Font credit https://github.com/keshikan/DSEG Release 7 
  
All information is For Indication only.  
No association, affiliation, recommendation, suitability, fitness for purpose should be assumed or is implied.  
Registered trademarks are owned by their respective registrants.  
