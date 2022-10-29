from datetime import datetime
import sys
import time
from typing import List, Optional

import RPi.GPIO as io

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

from user_input import (
    DEVICE_NUMBER,
    TOPIC,
    LED_PIN,
    SWITCH_PIN
)
from constants import LOG_MAIN
from utils import log

AWS_ENDPOINT = "aka77kba04erw-ats.iot.eu-west-1.amazonaws.com"
AWS_CA_FILE = "/home/certificates/AmazonRootCA1.pem"
AWS_KEY = "/home/certificates/private.pem.key"
AWS_CERT = "/home/certificates/certificate.pem.crt"
AWS_CLIENT_NAME = f'done{DEVICE_NUMBER}'
AWS_TOPIC = f"topic/{TOPIC}"

class IoTAWSStreaming():
    """Class to handle data collection from a reed sensor and streaming into AWS.

    Attributes:
        mode: Controls output location of the sensor data.
            Currently supports: local
        switch_pin: GPIO pin to communicate with the reed sensor.
        led_pin: GPIO pin to control the LED.
        local_log_path: Full path to store the readout data in local mode.
            Is required if 'local' is part of `mode`.
        deadtime: Readout dead time to protect the sensor in seconds.
            Defaults to 1 second.
    """
    supported_modes = ['local', 'aws']

    def __init__(
        self,
        mode: List[str],
        switch_pin: int,
        led_pin: int,
        local_log_path: str,
        deadtime: float = 1.0,
    ) -> None:
        self._local_log_path = local_log_path
        self._mode = IoTAWSStreaming._validate_mode(mode=mode, local_log_path=local_log_path)
        self._switch_pin = IoTAWSStreaming._validate_pin(pin=switch_pin)
        self._led_pin = IoTAWSStreaming._validate_pin(pin=led_pin)
        self._deadtime = IoTAWSStreaming._validate_deadtime(deadtime=deadtime)

    @classmethod
    def _validate_mode(cls, mode: List[str], local_log_path: Optional[str] = None) -> List[str]:
        """Class method to validate user input.

        Args:
            mode: Mode input argument.
            local_log_path: Full path to store the readout data in local mode.

        Returns:
            Mode if it is a part of the supported modes.

        Raises:
            ValueError if the user input is not supported.
        """
        try:
            assert isinstance(mode, list)
            for set_mode in mode:
                assert set_mode in IoTAWSStreaming.supported_modes
        except AssertionError:
            errmsg = f'Mode {mode} is not among the supported modes {IoTAWSStreaming.supported_modes}.'
            raise ValueError(errmsg) from AssertionError

        # Make sure that a file path for local storage is set
        if 'local' in mode:
            try:
                assert isinstance(local_log_path, str)
            except AssertionError:
                errmsg = f'local mode requires `local_log_path` which is {local_log_path} and this is not valid.'
                raise ValueError(errmsg) from AssertionError

        return mode

    @classmethod
    def _validate_pin(cls, pin: int) -> int:
        """Class method to validate user input.

        Args:
            pin: pin input argument.

        Returns:
            Pin if it is valid.

        Raises:
            ValueError if the user input is not supported.
        """
        try:
            assert isinstance(pin, int)
            assert pin > 0
            assert pin < 40

        except AssertionError:
            errmsg = f'Pin {pin} is supported. Must be smaller 40 and larger 0.'
            raise ValueError(errmsg) from AssertionError

        return pin

    @classmethod
    def _validate_deadtime(cls, deadtime: float) -> float:
        """Class method to validate user input.

        Args:
            deadtime: Deadtime input argument.

        Returns:
            deadtime if it is valid.

        Raises:
            ValueError if the user input is not supported.
        """
        try:
            assert isinstance(deadtime, float)
            assert deadtime > 0.0
            assert deadtime < 5.0

        except AssertionError:
            errmsg = f'Deadtime {deadtime} is supported. Must be float and between 0 and 5.0.'
            raise ValueError(errmsg) from AssertionError

        return deadtime

    def _setup_rpi(self) -> None:
        """Method to set up the GPIO on the RaspberryPi.
        """
        # Set Broadcom mode so we can address GPIO pins by number.
        io.setmode(io.BCM)

        # Set LED pin
        io.setup(self._led_pin, io.OUT)
        msg = f'Set up GPIO, using led pin {self._led_pin}'
        log(log_path=LOG_MAIN, logmsg=msg, printout=True)

        # Set wheel pin
        io.setup(self._switch_pin, io.IN, pull_up_down=io.PUD_UP)
        msg = f'Set up GPIO, using wheel pin {self._switch_pin}'
        log(log_path=LOG_MAIN, logmsg=msg, printout=True)

    def setup_aws(self) -> AWSIoTMQTTClient:
        """Method to set up communication with AWS.

        """
        mqtt_client = AWSIoTMQTTClient(AWS_CLIENT_NAME)
        mqtt_client.configureEndpoint(AWS_ENDPOINT, 8883)

        mqtt_client.configureCredentials(
            CAFilePath=AWS_CA_FILE,
            KeyPath=AWS_KEY,
            CertificatePath=AWS_CERT
        )
        return mqtt_client
    
    def send_message(self, topic: str, message: str, mqtt_client: AWSIoTMQTTClient) -> None:
        """Method to send a message to the AWS mqtt endpoint.

        Args:
            topic: Topic to publish to.
            message: Message to send.
            mqtt_client: MQTT connection.
        """

        now = datetime.now().strftime("%Y-%m-%d %I:%M:%S")
        mqtt_client.publish(
            topic,
            "{\"Timestamp\" :\"" + str(now) +
            "\", \"Message\":\"" + message + "\"}", 0)
        msg = f'Published to topic {topic} with message {message}.'
        log(log_path=LOG_MAIN, logmsg=msg, printout=True)
        

    def readout(self) -> None:
        """Method to start the readout of the reed sensor.

        If readout mode 'local', puts pin_state in the logfile.
        If readout mode 'aws', sends message to specified endpoint.
        """
        # Set GPIO
        self._setup_rpi()
        # Set AWS if selected
        if 'aws' in self._mode:
            mqtt_client = self.setup_aws()
            mqtt_connection = mqtt_client.connect()

        msg = 'Started script...'
        log(log_path=LOG_MAIN, logmsg=msg, printout=True)
      
        try:
            # Readout loop
            while True:
                msg = 'Running...'
                log(log_path=LOG_MAIN, logmsg=msg, printout=True)
                time.sleep(self._deadtime)
                if io.input(self._switch_pin) == 0:
                    msg = '0'
                    if 'local' in self._mode:
                        # Turn LED on
                        io.output(self._led_pin, io.HIGH)
                        log(log_path=self._local_log_path, logmsg=msg, printout=True)
                    if 'aws' in self._mode:
                        if mqtt_client is None:
                            msg = 'Error, MQTT client not initialized.'
                            log(log_path=LOG_MAIN, logmsg=msg, printout=True)
                        else:
                            self.send_message(topic=AWS_TOPIC, message=msg, mqtt_client=mqtt_client)
                else:
                    msg = '1'
                    if 'local' in self._mode:
                        # Turn LED off
                        io.output(self._led_pin, io.LOW)  
                        log(log_path=self._local_log_path, logmsg=msg, printout=True)
                    if 'aws' in self._mode:
                        if mqtt_client is None:
                            msg = 'Error, MQTT client not initialized.'
                            log(log_path=LOG_MAIN, logmsg=msg, printout=True)
                        else:
                            self.send_message(topic=AWS_TOPIC, message=msg, mqtt_client=mqtt_client)

        except KeyboardInterrupt:
            io.cleanup()
            if mqtt_client:
                mqtt_client.disconnect()
            sys.exit()


if __name__ == "__main__":
    iotawsstreaming = IoTAWSStreaming(
        mode=['local', 'aws'],
        switch_pin=SWITCH_PIN,
        led_pin=LED_PIN,
        deadtime=1.0,
        local_log_path=LOG_MAIN
    )
    iotawsstreaming.readout()
