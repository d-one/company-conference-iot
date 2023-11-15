"""
===================================================================================================
Author:      Stepan Gaponiuk - D ONE - 2023
Description: Quick test for the GPIO lib
===================================================================================================
"""
import sys
import time

LED_PIN = 4

try:
    import RPi.GPIO as GPIO

    # Set the GPIO modes
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

    # Test the LED
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(1)

    # Clean up and exit with success code
    GPIO.cleanup()
    sys.exit("RPi.GPIO installed and tested successfully")

except ImportError:
    sys.exit("RPi.GPIO library not found.")

except Exception as e:
    sys.exit(f"RPi.GPIO tested with and error: {e}")
