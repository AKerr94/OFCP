__author__ = "Alastair Kerr"

import MySQLdb

import config


class Database(object):
    """
    Middle-man between server and database handling requests
    Reads and writes entries for games as required
    """
    def __init__(self):
        """
        Initialise database settings from config
        """
        self.HOST = config.database_config['HOST']
        self.PORT = config.database_config['PORT']
        self.USER = config.database_config['USER']
        self.PASS = config.database_config['PASS']
        self.DB = config.database_config['DB']

    def execute_query(self, query):
        """
        Sanitises query then connects to database and executes given query
        :param query: string SQL query
        :return: None
        """
        query = self.sanitise_query(query)

        db = MySQLdb.connect(host=self.HOST,
                             port=self.PORT,
                             user=self.USER,
                             passwd=self.PASS,
                             db=self.DB)
        db.autocommit(True)

        cur = db.cursor()
        cur.execute(query)

        db.close()

    def sanitise_query(self, query):
        """
        Sanitises query to prevent SQL injection
        :param query: String SQL query
        :return: Sanitised query
        """
        return MySQLdb.escape_string(query)
