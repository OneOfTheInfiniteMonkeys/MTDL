# MTDL (MagTag Data Logger) - {Pre-Release}
MagTag Temperature Data Logger permits ambient temperature monitoring in the environment of the device, using an internal sensor on the MagTags PCB (other data could readily be logged). With minmimal calibration, obviates the need for additional external hardware. Typically 1 C resolution, ±1 C accuracy, ~0.35 C / minute for a 5 C step change, range -20 to +60 C. Based on Adafruit example code. Additional features include Segment numeric indicator and data graphing on the e-ink display of the <a href="https://www.adafruit.com/product/4800" target="_blank">Adafruit Magtag</a> device.

<div align="center">
  <div style="display: flex; align-items: flex-start;">
  <img src="https://raw.githubusercontent.com/OneOfTheInfiniteMonkeys/MTDL/main/images/20230205-MTDL-Beta.jpg" width="400px" alt="Adafruit Magtag Data Logger PCB. Image copyright (c) 05 Feb 2023 OneOfTheInfiniteMonkeys All Rights Reserved">
  </div>
</div>  

[![Language](https://img.shields.io/static/v1?label=CircuitPython&message=7.3.0&color=blueviolet&style=flat-square)](https://circuitpython.org/board/adafruit_magtag_2.9_grayscale/)
[![Language](https://img.shields.io/static/v1?label=CircuitPython&message=8.0.0-beta.6&color=blueviolet&style=flat-square)](https://circuitpython.org/board/adafruit_magtag_2.9_grayscale/)
[![MagTag](https://img.shields.io/badge/gadget-MagTag-blueviolet.svg?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgdmlld0JveD0iMTIgMTIgNDAgNDAiPjxwYXRoIGZpbGw9IiMzMzMzMzMiIGQ9Ik0zMiwxMy40Yy0xMC41LDAtMTksOC41LTE5LDE5YzAsOC40LDUuNSwxNS41LDEzLDE4YzEsMC4yLDEuMy0wLjQsMS4zLTAuOWMwLTAuNSwwLTEuNywwLTMuMiBjLTUuMywxLjEtNi40LTIuNi02LjQtMi42QzIwLDQxLjYsMTguOCw0MSwxOC44LDQxYy0xLjctMS4yLDAuMS0xLjEsMC4xLTEuMWMxLjksMC4xLDIuOSwyLDIuOSwyYzEuNywyLjksNC41LDIuMSw1LjUsMS42IGMwLjItMS4yLDAuNy0yLjEsMS4yLTIuNmMtNC4yLTAuNS04LjctMi4xLTguNy05LjRjMC0yLjEsMC43LTMuNywyLTUuMWMtMC4yLTAuNS0wLjgtMi40LDAuMi01YzAsMCwxLjYtMC41LDUuMiwyIGMxLjUtMC40LDMuMS0wLjcsNC44LTAuN2MxLjYsMCwzLjMsMC4yLDQuNywwLjdjMy42LTIuNCw1LjItMiw1LjItMmMxLDIuNiwwLjQsNC42LDAuMiw1YzEuMiwxLjMsMiwzLDIsNS4xYzAsNy4zLTQuNSw4LjktOC43LDkuNCBjMC43LDAuNiwxLjMsMS43LDEuMywzLjVjMCwyLjYsMCw0LjYsMCw1LjJjMCwwLjUsMC40LDEuMSwxLjMsMC45YzcuNS0yLjYsMTMtOS43LDEzLTE4LjFDNTEsMjEuOSw0Mi41LDEzLjQsMzIsMTMuNHoiLz48L3N2Zz4%3D&style=flat-square)](https://github.com/adafruit/Adafruit_MagTag_PCBs)
![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/OneOfTheInfiniteMonkeys/MTDL?&include_prereleases&style=flat-square)
[![GitHub License](https://img.shields.io/github/license/OneOfTheInfiniteMonkeys/MTDL?style=flat-square)](https://github.com/OneOfTheInfiniteMonkeys/MTMP/blob/main/LICENSE) 
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=flat-square)](https://github.com/OneOfTheInfiniteMonkeys/moreinfo/graphs/commit-activity)
![GitHub repo size](https://img.shields.io/github/repo-size/OneOfTheInfiniteMonkeys/MTDL?style=flat-square)

## Introduction
The CircuitPython implementation of the MagTag Data Logger is intended to allow ambient e.g. room temperature monitoring without need for additional sensing hardware. The software permits logging and on board graphing of the measured temperature. For accurate measurements a reference temperature point needs to be established, perhaps with reference to an existing room sensor (see Calibration section). This opreation should only be required once. Where relative temperatures are satisfactory, no calibration is necessary. Other data from a variety of sources could be logged with relatively minor modification.

## Installation
Requirements
- <a href="https://www.adafruit.com/product/4800" target="_blank">Adafruit Magtag</a>
- <a href="https://www.adafruit.com/product/4236" target="_blank">Adafruit LiPo Cell (typical)</a>
- <a href="https://downloads.circuitpython.org/bin/adafruit_magtag_2.9_grayscale/en_GB/adafruit-circuitpython-adafruit_magtag_2.9_grayscale-en_GB-7.3.0.uf2" target="_blank">CicruitPython 7.3.0</a>

Optional  
- <a href="https://en.wikipedia.org/wiki/USB-C" target="_blank">USB cable connection to host computer</a>

Copy the files located in the dist folder to the CIRCUITPY folder of the Adafruit MagTag.  

Note 
- The implementation can use WiFi and thus a secrets.py file should typically have any entries, it must be in the CIRCUITPY drive .
- Following release of <a href="https://github.com/adafruit/circuitpython/releases" target="_blank">CircuitPython 7</a> to stable, the code implements switch off of HID disk and serial ports via boot.py.
- If electing to use alternate CircuitPython releases <a href="https://github.com/adafruit/circuitpython/releases" target="_blank"> e.g. CircuitPython 7.1.x etc.</a> you need to replace the lib .mpy files with the release counterparts in the lib folder.
- The '<a href="https://github.com/OneOfTheInfiniteMonkeys/MTDL/blob/main/Magtag%20PowerPoint%20Layout%2003.pptx">Magtag PowerPoint Layout 03.pptx</a>' file is a Microsoft&trade; PowerPoint&trade; pack with slidemaster backgrounds consisting of a Magtag graphic to enable graphic design prior to coding. The image scale approximates to 2:1 The file should load into Google&trade; Docs, though this has not be tested.
- Ensure any temperature changes result in no condensation in or on the electronics
- LiPo cells may degrade at temperature extremes
- Display may not operate at low temperatures, the software is coded to omit updates below -9 C
- Operation outside the manufacturers specification(s) for any component must not occur

## Hardware
Important - Required for use is a small <a href="https://www.adafruit.com/product/4236" target="_blank">LiPo</a> battery, supported by the MagTag.  
Suggested - <a href="https://www.adafruit.com/product/4807" target="_blank">Acrylic + Hardware Kit for Adafruit MagTag<a>  

## Discussion
Design of the MagTag means that when the unit is powered from the USB port the on board voltage regulator and ESP32-S2 cause the units PCB to heat, To approximately 33 C with a room ambient of 21 C under typical use conditions. This heating effect (see image below) causes a measurement error and unless the PCB temperature is desired, powering from the USB port typically prevents ambient temperature sensing due to heat soak from the ESP32-S2 and voltage regulators.  

<div align="center">
  <div style="display: flex; align-items: flex-start;">
  <img src="https://raw.githubusercontent.com/OneOfTheInfiniteMonkeys/MTDL/main/images/MagTag-Thermal-USB-Powered-00.jpg" width="400px" alt="Adafruit Magtag Data Logger PCB with USB power, Thermal Image. Image copyright (c) 04 Feb 2023 OneOfTheInfiniteMonkeys All Rights Reserved. Emisivity set for PCB, room ambient 22 C">
  </div>
</div>  

Use of magnetic stand off feet to attach the MagTag to a metallic surface will modify the devices temperature responsiveness. Provided the attachment point moves largely with the environment (room) the impact should be relatively limited, if somewhat slower than the air temperature change.

For sensing of the ambient temperature, air flow over the rear of the MagTag should ideally not be restricted. Testing within a <a href="https://raw.githubusercontent.com/OneOfTheInfiniteMonkeys/MTMP/main/images/MagTag-MacroPad-00.png" target="_blank">plastic<a> case the MagTag was attached to demonstrated reasonable thermal sensitivity.  

An external temperature (or other) sensor(s) could readily be substituted, via the MagTags data connections if desired.

All information is For Indication only.  
No association, affiliation, recommendation, suitability, fitness for purpose should be assumed or is implied.  
Registered trademarks are owned by their respective registrants.  
