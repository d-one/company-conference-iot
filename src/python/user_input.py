"""
===================================================================================================
Author:      Heiko Kromer - D ONE 2022
Description: This script contains user input for the company conference workshop IoT
===================================================================================================
"""
# General
USER_NAME = 'animalX'  # Add your user name here

# GPIO
LED_PIN = 26  # GPIO pin where the LED is connected to
SWITCH_PIN = 4  # GPIO pin where the reed switch is connected to

# Azure

# AWS
DEVICE_NUMBER = 'X'  # Add your device number here, e.g., done4
AWS_ENDPOINT = 'xxxxxxxxxxxxxxx-ats.iot.eu-central-1.amazonaws.com'  # Add the endpoint here
AWS_CA_FILE = '/home/xxx/xxx/AmazonRootCA1.pem'  # Add path to the CA here
AWS_KEY = '/home/xxx/xxx/private.pem.key'  # Add path to the private key here
AWS_CERT = '/home/xxx/xxx/certificate.pem.crt'  # Add path to the certificate here

AWS_CLIENT_NAME = f'done{DEVICE_NUMBER}'  # DO NOT EDIT THIS
AWS_TOPIC = f'topic/{AWS_CLIENT_NAME}'  # DO NOT EDIT THIS
