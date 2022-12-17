#!/usr/bin/env python

import logging
from time import sleep
from threading import Event
from prometheus_client import start_http_server, REGISTRY
import RPi.GPIO as GPIO

from collector import Collector

event = Event()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Tell GPIO library to use GPIO references
GPIO.setmode(GPIO.BCM)

logger.info('Setup GPIO pin as input on GPIO17')

# Set Switch GPIO as input
# Pull high by default
GPIO.setup(17 , GPIO.IN, pull_up_down=GPIO.PUD_UP)

# GPIO.add_event_detect(17, GPIO.BOTH, callback=sensorCallback, bouncetime=200)

if __name__ == "__main__":

    REGISTRY.register(Collector(logger))

    start_http_server(9984)

    while True:
        try:
            sleep(10)
        except KeyboardInterrupt:
            # Reset GPIO settings
            GPIO.cleanup()
            event.set()
            break
