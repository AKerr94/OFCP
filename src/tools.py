__author__ = "Alastair Kerr"

from datetime import datetime


def get_formatted_datetime():
    """
    Date and time to the second as formatted string
    :return: String
    """
    return str(datetime.now())[:-7]