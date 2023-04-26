#!/usr/bin/env python3
"""filtered_logger module
"""
import re
import logging
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """filtered_logger function that,
    given a list of fields, replaces them with a redaction

    Args:
        fields (list): list of strings representing
        all fields to obfuscate
        redaction (str): string representing by
        what the field will be obfuscated
        message (str): string representing the log line

    Returns:
        str: log message obfuscated
    """
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """init function

        Args:
            fields (list): list of strings representing
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format function that filter values in incoming log records
        using filter_datum function

        Args:
            record (logging.LogRecord): log record

        Returns:
            str: log message obfuscated
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """get_logger function that takes no arguments and
    returns a logging.Logger object

    Returns:
        logging.Logger: object
    """
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger = logging.getLogger("user_data").setLevel(
        logging.INFO).addHandler(handler)
    logger.propagate = False
    return logger
