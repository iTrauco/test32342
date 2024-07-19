# tests/test_hello.py

import pytest
from utils.logging_utils import setup_logger

# Initialize the logger
logger = setup_logger()

def test_example():
    logger.info("Starting test_example")
    assert True
