import json
import logging
import os
import sys
from io import StringIO
import pytest

_beautiful_json = dict(indent=2, ensure_ascii=False, sort_keys=True)

# LOGGING ####################################################################################################
# Logger formatting
log_formatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s] - %(message)s",
                                  datefmt='%Y-%m-%d %H:%M:%S')


class CustomLogger(logging.Logger):
    def __init__(self, *args, **kwargs):
        self.test_log = StringIO()
        super().__init__(*args, **kwargs)

    # Method formatting message
    @staticmethod
    def format_message(message):
        return json.dumps(message, **_beautiful_json) if isinstance(message, (dict, list, tuple)) else str(message)

    # Method to attached data to report (one class dependency)
    def attach_debug(self, name, message):
        if self.isEnabledFor(10):
            pytest.allure.attach(name, self.format_message(message))

    def attach_info(self, name, message):
        if self.isEnabledFor(20):
            pytest.allure.attach(name, self.format_message(message))

    def attach_error(self, name, message):
        pytest.allure.attach(name, self.format_message(message))


def setup_logging():
    # Logging setup
    _logger = CustomLogger('root')

    # Level of handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(os.getenv('LOGGING_LEVEL_TO_CONSOLE', 'WARN'))
    # Create a method of message
    console_handler.setFormatter(log_formatter)
    _logger.addHandler(console_handler)

    # Level of handler
    string_io = logging.StreamHandler(_logger.test_log)
    string_io.setLevel(os.getenv('LOGGING_LEVEL', 'INFO'))
    # Create a method of message
    string_io.setFormatter(log_formatter)
    _logger.addHandler(string_io)
    return _logger


logger = setup_logging()
