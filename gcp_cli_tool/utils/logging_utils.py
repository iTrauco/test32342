# gcp_cli_tool/utils/__init__.py
from .logging_utils import setup_logger
# gcp_cli_tool/utils/logging_utils.py

import logging
import os

# gcp_cli_tool/utils/logging_utils.py

import logging
import os

def setup_logger(log_file='test_results.log'):
    """Set up a logger to output messages to a file."""
    # Ensure the logs directory exists
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure the logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger
