========================================
About
========================================
GPSDemo.py is a demo for the Terminus GSM864Q that reports GPS
coordinates, signal strength, and a sawtooth algorithm value
to the Exosite platform.

Terminus GSM864Q product details: 
http://www.janus-rc.com/terminusgsm.html

Exosite info:
http://exosite.com

License is BSD, Copyright 2010, Exosite LLC

Third-party license and copyright info is contained on the appropriate files.

========================================
Quick Start
========================================
****************************************
1) Enter your Applications Specific Configuration settings
****************************************
Enter your info as indicated in the GPSDemo.py file.

To obtain a CIK value, you must have an Exosite account and a
device configured through Exosite Portals.

If you need an Exosite account, create a free account at:
https://one.exosite.com/signup

To setup a device, refer to the documentation:
http://exosite.com/developers/documentation?cid=1009


****************************************
2) Compile and download the updated files to the device
****************************************
Compile ALL the files included in the 'src' directory and
move the compiled versions into the 'compiled' directory.

Download all of these compiled files onto the device.

See product documentation for instructions on how to compile
and download files.


****************************************
3) Setup the GPSDemo.py as the startup script
****************************************
Connect to the device and execute the AT command:
AT#ESCRIPT = "GPSDemo.pyo"

Then unplug the device to reboot it.  The script should begin
running automatically after powering the device back on.

