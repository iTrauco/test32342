# gcp_cli_tool/tests/test_hello.py
import logging

# Configure logging
logging.basicConfig(filename='test_results.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_hello_function():
    try:
        # Your test logic here
        assert 1 + 1 == 2
        logging.info("test_hello_function passed")
    except AssertionError:
        logging.error("test_hello_function failed")
