import json
import logging
import os
from datetime import datetime as dt

"""
A file with loggers, which are useful for storing logs (on ELK, for example)
And displaying them in console simultaneously
"""


def configure(logger: logging.Logger):
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(filename=os.getenv('SERVER_LOGS'))
    console_handler = logging.StreamHandler()

    file_handler.setFormatter(JSONFormatter())
    console_handler.setFormatter(StringFormatter())

    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


class JSONFormatter(logging.Formatter):
    """A formatter for JSON - formatted log messages"""

    def format(self, record: logging.LogRecord) -> str:
        if record.exc_info is not None:
            message = self.formatException(record.exc_info)
        else:
            message = record.getMessage()
        return json.dumps({
            'name': record.name,
            'level': record.levelname,
            'pathname': record.pathname,
            'line': record.lineno,
            'timestamp': dt.utcnow().isoformat(),
            'message': message,
        }, ensure_ascii=False)


class StringFormatter(logging.Formatter):
    def __init__(self):
        super(StringFormatter, self).__init__()

    def format(self, record: logging.LogRecord) -> str:
        if record.exc_info is not None:
            message = self.formatException(record.exc_info)
        else:
            message = record.getMessage()
        return f'{record.name}:{record.pathname}:{record.lineno} {dt.utcnow().isoformat()}:[{record.name}:{record.levelname}] {message}'
