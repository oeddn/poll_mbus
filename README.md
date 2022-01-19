# poll_mbus

Python script for reading data from devices on a serial **Meter-Bus (NOT Modbus!)**.

## Current usage scenario:
- read data from multiple devices on a serial Meter-Bus using the libmbus Library from <https://github.com/rscada/libmbus> (install first)
- parse output for the values of interest
- write values to one .csv file per device and month
	- if the file already exists, data is appended to that file
	- new file per month, to keep file sizes small

## Supported device output
- EASTRON SDM230-MBus single phase active import/export energy meter
- engelmann SENSOSTAR U heat flow meter with optional Meter-Bus Interface

Theres a class for every supported device. It should be easy to add more once you know which data fields you want to read from your device.

## Hardware
I use a DIY Meter-Bus master built on protoboard, similar to the one shown here: <https://github.com/rscada/libmbus/hardware/MBus_USB.pdf>

As USB-serial converter I use a cheapo USB-Plug style Adapter with open ends, that I connected to pin headers on the protoboard. The chipset is a PL2303, unfortunately without a unique serial number (no, it is not programmable either), so that more than one adapter of the same type can not easily be distinguished, e.g. to use udev rules (Linux). As a workaround you can:
- buy adapters with unique serial numbers (this might get tricky and/or expensive)
- use different adapters, so that vendor and/or product id differ
- plug in devices in a specific order after (re)boot
- distinguish them by using the port number of a USB Hub (my choice). I will add a link when I have completed the description for that.
