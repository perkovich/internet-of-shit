#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import requests
import logging
requests.packages.urllib3.disable_warnings()
logging.basicConfig(filename='range.log', format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)


def sort_and_truncate(measurements):
    """Return sorted measurements without smallest and largest values."""
    sorted_measurements = sorted(measurements)
    return sorted_measurements[1:-1]


def truncated_median(measurements):
    """Returns the median of a list of measurements."""
    truncated = sort_and_truncate(measurements)
    n_measurements = len(truncated)
    middle = n_measurements / 2
    if n_measurements % 2 == 0:
        # Median of an aven length list is the average of the two
        # middle elements.
        return sum(truncated[middle - 1:middle + 1]) / 2.0
    else:
        return truncated[middle]


def truncated_mean(measurements):
    """Return the truncated mean of a list of measurements."""
    truncated = sort_and_truncate(measurements)
    total = sum(truncated)
    return total / len(truncated)


GPIO.setmode(GPIO.BCM)

NUMBER_OF_MEASUREMENTS = 5
TRIG = 23
ECHO = 24

print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


distances = []
for loop in range(NUMBER_OF_MEASUREMENTS):
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
    distances.append(distance)

print "Median:", truncated_median(distances)
print "Mean:", truncated_mean(distances)

url = "https://10.0.176.23/json.htm?type=command&param=udevice&idx=68&nvalue=0&svalue="
distance = str(distance)
url = url + distance 
print url
requests.get(url, verify=False)

GPIO.cleanup()
