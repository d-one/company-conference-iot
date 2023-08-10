import time
import RPi.GPIO as io
import sys
import json
from user_input import LED_PIN, SWITCH_PIN
from azure.iot.device import IoTHubDeviceClient, Message
import os
home_dir = os.path.expanduser()
print(home_dir)
# adding external folder with Azure constr to python path for import
def read_azure_connection_string(path: str, connection_string_name: str) -> str:
    """Function to read the Azure connection string from a file.
    If the connection string is not found, the function will raise an exception."""
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith(connection_string_name):
                return line.split("=")[1].strip()
    raise Exception(f"Azure Connection string {connection_string_name} not found in file {path}")
        
def read_azure_device_id(path: str, device_id_name: str) -> str:
    """Function to read the Azure device id from a file.
    If the device id is not found, the function will raise an exception."""
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith(device_id_name):
                return line.split("=")[1].strip()
    raise Exception(f"Azure Device ID {device_id_name} not found in file {path}")
        
# setting the connection string and device name using values from the file
azure_config_filepath = f'{home_dir}/azure_constr.txt'
connection_string = read_azure_connection_string(path=azure_config_filepath, connection_string_name="CONNECTION_STRING")
device_id = read_azure_device_id(path=azure_config_filepath, device_id_name="DEVICE_ID")

# Set Broadcom mode so we can address GPIO pins by number.
io.setmode(io.BCM)
io.setup(SWITCH_PIN, io.IN, pull_up_down=io.PUD_UP)
io.setup(LED_PIN, io.OUT)

# Define the JSON message variables to send to IoT Hub.
messageEpoch = time.time()
magnet = 0

def iothub_client_init():
    # Create an IoT Hub client using protocol MQTT v3.1.1 over WebSocket on port 443.
    client = IoTHubDeviceClient.create_from_connection_string(connection_string, websockets=True) 
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        while True:
            # Build the message with magnet telemetry values.
            messageEpoch = time.time()
            time.sleep(1)
            if (io.input(SWITCH_PIN) == 0):
                magnet = 1
                io.output(LED_PIN, io.HIGH)
                msg_dict = {"messageEpoch": messageEpoch, "deviceID": device_id, "magnet": magnet, "pin_num": SWITCH_PIN}
                message = Message(json.dumps(msg_dict))
                # ensure proper encoding and content type are enforced (again to avoid de-serialization issues)
                message.content_encoding = "utf-8"
                message.content_type = "application/json"

                # Send the message.
                print( "Sending message: {}".format(message) )
                client.send_message(message)
                print ( "Message successfully sent" )
            else:
                magnet = 0
                io.output(LED_PIN, io.LOW)
                # needs to be a python dict, otherwsie de-serialization errors will occur on Azure sid
                msg_dict = {"messageEpoch":messageEpoch, "deviceID":deviceID, "magnet":magnet, "pin_num":SWITCH_PIN}
                message = Message(json.dumps(msg_dict))
                # ensure proper encoding and content type are enforced (again to avoid de-serialization issues)
                message.content_encoding = "utf-8"
                message.content_type = "application/json"

                # Send the message.
                print( "Sending message: {}".format(message) )
                client.send_message(message)
                print ( "Message successfully sent" )

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )
        io.cleanup()
        sys.exit()

if __name__ == '__main__':
    print ( "Azure IoT Workshop - Raspberry PI device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
