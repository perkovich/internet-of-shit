#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import requests
import logging
requests.packages.urllib3.disable_warnings()
logging.basicConfig(filename='range.log', format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)

GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24

print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(2)

GPIO.output(TRIG, True)
time.sleep(0.001)
GPIO.output(TRIG, False)

while GPIO.input(ECHO)==0:
  pulse_start = time.time()

while GPIO.input(ECHO)==1:
  pulse_end = time.time()

pulse_duration = pulse_end - pulse_start

distance = pulse_duration * 17150

distance = round(distance, 2)
logging.warning(distance)

print "Distance:",distance,"cm"

url = "https://10.0.176.23/json.htm?type=command&param=udevice&idx=68&nvalue=0&svalue="
distance = str(distance)
url = url + distance 
print url
requests.get(url, verify=False)

GPIO.cleanup()
