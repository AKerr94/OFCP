__author__ = "Alastair Kerr"

from datetime import datetime
import ast

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

def load_dictionary_from_string(obj):
    """
    Used to evaluate a string representation of a dictionary
    :param obj: String representation of a dictionary
    :return: Dictionary
    """
    return ast.literal_eval(obj)


def render_template(template, env, **kwargs):
    """
    Returns HTML rendered from template with passed args
    :param template: Filename in templates/
    :param kwargs: Variables used in template
    :return: Rendered template
    """
    t = env.get_template(template)
    return t.render(**kwargs)
