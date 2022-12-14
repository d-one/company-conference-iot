"""
===================================================================================================
Author:      Heiko Kromer - D ONE - 2022
Description: This script contains functionality to make an LED attached to an Raspberry Pi 4 blink
===================================================================================================
"""
import sys
import time
import logging
import RPi.GPIO as GPIO
from user_input import LED_PIN

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Bring LED to blink for 30 seconds, one second intervals
try:
    cnt = 0
    while cnt < 30:
        GPIO.output(LED_PIN, GPIO.HIGH)
        logger.info("## Turned LED ON.")
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
        logger.info("## Turned LED OFF.")
        time.sleep(1)
        cnt += 1
    logger.info("## Done with the blinking!")
    GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
