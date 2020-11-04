import machine
from machine import Pin, ADC

import dht
import network
import urequests
from time import sleep

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = '<your_wifi_ssid_here>'
password = '<your_wifi_password_here>'
api_key = '<your_google_sheets_apikey_here>'

# You also need to change "esp_logger" to the trigger you named in the IFTTT applet in the request url below.

# define pin for the sensor (define DHTtype and pin)
sensor = dht.DHT22(Pin(27))

# define pin for analog pin for battery
# batt = ADC(Pin(34)) # create ADC object on ADC pin
#batt_lvl = batt.read() # read value, 0-4095 across voltage range 0.0v - 1.0v
#batt.atten(ADC.ATTN_11DB) # set 11dB input attentuation (voltage range roughly 0.0v - 3.6v)
#batt.width(ADC.WIDTH_9BIT) # set 9 bit return values (returned range 0-511)
#batt_lvl = batt.read() # read value using the newly configured attenuation and width
#print('the battery level is:')
#print(batt_lvl)

ms_sleep_time = 1800000

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass    

print('Connection successful')
print(station.ifconfig())
sleep(5)


def deep_sleep(msecs) :
    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after X milliseconds (waking the device)
    rtc.alarm(rtc.ALARM0, msecs)

    # put the device to sleep
    machine.deepsleep()


def read_sensor():
    global temp, hum
    temp = hum = 0
  
    try:
        sensor.measure()
        sleep(1)
        temp = sensor.temperature()
        hum = sensor.humidity()

        if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
            msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))

            # uncomment for Fahrenheit
            #temp = temp * (9/5) + 32.0
            
            hum = round(hum, 2)
            print('its a float')
            return(msg)
        else:
            # if values aren't floats or ints
            return('invalid readings, trying again')
            print('its not a float')

    except OSError as e:
        print('its an error')
        return('Failed to read/publish sensor readings.')


read_sensor() # Get readings from the sensor the first time


while True:
    try:
        if (type(temp) is float and type(hum) is float):
            sensor_readings = {'value1':temp, 'value2':hum, 'value3':batt_lvl}
            print(sensor_readings)

            request_headers = {'Content-Type': 'application/json'}

            request = urequests.post(
            'http://maker.ifttt.com/trigger/esp_logger/with/key/' + api_key, #make sure you change "esp_logger" to the trigger you named in the IFTTT applet
            json=sensor_readings,
            headers=request_headers)
            print(request.text)
            request.close()
            
            print('going to sleep soon')
            sleep(2)
            
            machine.deepsleep(ms_sleep_time) #ESP32
            break # Not sure if this break is needed
        else:
            read_sensor() # Get readings from the sensor again

    except OSError as e:
        print('Failed to read/publish sensor readings.')

