#!/usr/bin/env python3
"""filtered_logger module
"""
import logging
import os
import re
from typing import List
import mysql.connector


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
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """get_db function that returns a connector to the database

    Returns:
        mysql.connector.connection.MySQLConnection: connector to the database
    """
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(user=user, password=password,
                                   host=host, database=database)


def main():
    """main function that connects to the database and retrieves all rows
    in the users table and display each row under a filtered format
    """
    conn = get_db()
    logger = get_logger()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = "".join(f"{f}={str(r)}" for f, r in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
