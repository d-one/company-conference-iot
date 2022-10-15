"""
================================================================================
Author:      Heiko Kromer - D ONE 2022
Description: This script contains constants used in company-conference-iot
================================================================================
"""
from user_input import USER_NAME

# Flag to control if the script will be run locally on the Pi or from remote
_REMOTE = False

# RPi paths
HOME = f'/home/{USER_NAME}/'
REPO = 'company-conference-iot'
LOGS = '/logs/'

# Log file for the publishing of the ip
FILENAME_LOG_PUBLISHIP = 'publish_ip.log'
# Log file for the main part of the workshop
FILENAME_LOG_MAIN = 'main.log'
# Filename for the script to retrieve ifconfig results
FILENAME_GET_WLAN = 'get_wlan.sh'
# Path to the bash script to retrieve ifconfig results
BASH_GET_WLAN = f'/{REPO}/src/bash/{FILENAME_GET_WLAN}'

LOG_PUBLISHIP = f'{HOME}{LOGS}{FILENAME_LOG_PUBLISHIP}'
LOG_MAIN = f'{HOME}{LOGS}{FILENAME_LOG_MAIN}'
