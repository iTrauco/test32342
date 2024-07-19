# gcp_cli_tool/tests/test_hello.py

import pytest
import logging
from gcp_cli_tool.cli import cli
from gcp_cli_tool.utils.logging_utils import setup_logger  # 🚨🔧

# Set up logger
logger = setup_logger()  # 🚨🔧

def test_hello_command():
    """Test the hello command."""
    # Log the start of the test
    logger.info("Starting test_hello_command")  # 🚨🔧
    
    # Execute the CLI command and capture the output
    result = cli.invoke(['hello'])  # 🟠
    
    # Check the result
    assert result.exit_code == 0
    assert "Hello, world!" in result.output  # 🟠
    
    # Log the result
    logger.info("Finished test_hello_command with result: %s", result.output)  # 🚨🔧

# Ensure that pytest captures the log messages
@pytest.fixture(autouse=True)
def caplog(caplog):
    """Fixture to capture log messages."""
    with caplog.at_level(logging.INFO):
        yield caplog
