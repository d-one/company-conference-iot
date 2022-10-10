"""
================================================================================
Author:      Heiko Kromer - 2022
Description: This script contains constants used in company-conference-iot
================================================================================
"""
# Flag to control if the script will be run locally on the Pi or from remote
_REMOTE = False

# RPi paths
HOME = '/home/done2/'
REPO = 'company-conference-iot'
LOGS = '/logs/'

# Log file for the hamsterwheel readout code
FILENAME_LOG_PUBLISHIP = 'publish_ip.log'
# Filename for the script to retrieve ifconfig results
FILENAME_GET_WLAN = 'get_wlan.sh'
# Path to the bash script to retrieve ifconfig results
BASH_GET_WLAN = f'/{REPO}/src/bash/{FILENAME_GET_WLAN}'

LOG_PUBLISHIP = f'{HOME}{LOGS}{FILENAME_LOG_PUBLISHIP}'

# AWS
AWS_CLIENT_NAME = "doneX"
AWS_ENDPOINT = "aka77kba04erw-ats.iot.eu-west-1.amazonaws.com"
AWS_CA_FILE = "/home/certificates/AmazonRootCA1.pem"
AWS_KEY = "/home/certificates/private.pem.key"
AWS_CERT = "/home/certificates/certificate.pem.crt"
