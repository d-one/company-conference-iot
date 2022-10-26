"""
==================================================================================
Author:      Heiko Kromer - D ONE - 2022
Description: This script contains utility functions used in company-conference-iot
==================================================================================
"""
from io import TextIOWrapper
from typing import Tuple, Optional
from datetime import datetime
import logging
import sys
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def safe_open_folder(path: str, mode: str) -> TextIOWrapper:
    """Function to open "path" for writing, creating any parent directories as needed.

    Args:
        path: Path to open for creating any parent directories if needed.
        mode: OpenTextMode as per definition in python built-in function `open()`.

    Returns:
        TextIOWrapper object to use in place of `open()`.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    return open(path, mode)

def log(log_path: str, logmsg: str, printout: bool = False) -> None:
    """Function to add a line to a logfile.

    Args:
        log_path: Full path to the filename with the log.
        logmsg: Message to be appended to the log file.
        printout: If True, `logmsg` is also printed out. Defaults to False.

    Returns:
        None.
    """
    # Add the current timestamp to the log
    logmsg = f'{datetime.now()} - {logmsg}'

    if printout:
        logger.info(f"## Added log message: {logmsg}.")

    with safe_open_folder(path=log_path, mode='a+') as file:
        file.write('\n')
        file.write(logmsg)
        file.close()
