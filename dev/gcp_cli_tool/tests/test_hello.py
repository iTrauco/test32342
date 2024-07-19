# tests/test_hello.py
import pytest
from gcp_cli_tool.commands.hello import say_hello
from gcp_cli_tool.utils.logging_utils import setup_logger

# Setup logger
logger = setup_logger()

def test_say_hello():
    logger.info("Running test_say_hello")
    result = say_hello("World")
    assert result == "Hello, World!"
    logger.info("Test passed!")
