# A Temperature & humidity sensor for Humidors

A wireless Temperature & Humidity sensor implemented to be placed inside a Cigar Humidor using the ESP32 micro-controller.

## Description

This is a micropython script for the ESP32 which gets the **temperature** and **humidity** readings from the DHT22 (AM2301) sensor 
and periodically logs it to a google sheets document via IFTTT.

The ESP32 then enters **deep sleep** mode for a defined period of time and then repeats the process.

The **wifi** capabilities of the ESP32 allows it to be placed in enclosed containers without damaging it.

The ESP32's **deep sleep** mode allows it to be powered by a battery for a long period of time.

Coding in micropython is arguably easier than in Arduino.


## Requirements for a Humidor Sensor

- Measures both temperature and humidity.
- Wireless (No drilling needed for cabling.)
- A relatively small device.
- Low powered (Replace batteries every month or so.)
- Log to google sheets (max of 2000 rows); No need to manage a server though.

**Fun Fact**: Cigars should be preserved somewhere around 70f at a *relative* humidity of around 70%.

## Original guide here with a different sensor:

https://randomnerdtutorials.com/low-power-weather-station-datalogger-using-esp8266-bme280-micropython/

The original guide uses a different sensor that includes a pressure sensor.

Guides on flashing micropython are available in the original guides website.


## What you need

- an ESP32 board.
- a temperature/humidity sensor (this script uses the AM2301.)
- Some pin wires.
- a 4.7 ohm resistor.
- A usb cable for the board.
- Either a usb power bank or a 3.7v battery supply.


## steps

- Get a micropython IDE like **upycraft**.
- Get the latest micropython bin file.
- Install the ESP32 usb driver for your PC (Check your ESP32's specs, my driver was **CP210X**.)
- Flash the ESP32 with micropython using the IDE.
- Create a ifttt account (If this then that.)
- Create a ifttt applet for webhooks -> google sheets.
- Test the applet in the ifttt website.
- Create a file called boot.py and upload it to the ESP32.
- Make sure to change all parameters including the **triggername** for the IFTTT applet in the **url** request.