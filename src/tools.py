__author__ = "Alastair Kerr"

from datetime import datetime

import config


def get_formatted_datetime():
    """
    Date and time to the second as formatted string
    :return: String
    """
    return str(datetime.now())[:-7]

def write_error(message):
    """
    Writes error log to logs/error_logs with message
    :param message: Error message
    :return: None
    """
    with open('%s/error_logs' % config.LOGS_DIR, 'a') as f:
        f.write("%s: %s\n" % (get_formatted_datetime(), message))
