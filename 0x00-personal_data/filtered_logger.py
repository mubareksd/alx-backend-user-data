#!/usr/bin/env python3
"""filtered_logger module
"""
import re


def filter_datum(fields, redaction, message, separator):
    """given a list of fields, replaces them with a redaction
    """
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message
