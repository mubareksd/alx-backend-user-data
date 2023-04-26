#!/usr/bin/env python3
"""filtered_logger module
"""
import re


def filter_datum(fields, redaction, message, separator):
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
