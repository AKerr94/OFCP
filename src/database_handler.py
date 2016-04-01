__author__ = "Alastair Kerr"

import MySQLdb
from datetime import datetime

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
        Connects to database and executes given query
        :param query: string SQL query
        :return: Result of query
        """
        db = MySQLdb.connect(host=self.HOST,
                             port=self.PORT,
                             user=self.USER,
                             passwd=self.PASS,
                             db=self.DB)
        db.autocommit(True)

        cur = db.cursor()
        try:
            cur.execute(query)
            result = cur.fetchall()
        except Exception, e:
            db.close()
            error = "%s: %s" % (datetime.now(), e)
            with open('%s/error_logs' % config.LOGS_DIR, 'a') as f:
                f.write("%s: There was an error executing an SQL query!" % datetime.now())
                f.write(error)
            return error

        db.close()
        return result

    def build_query(self, query, *params):
        """
        Perform basic sanitisation to avoid SQL injection and build full query
        :param query: Query with %s for any params
        :param params: List of values to insert into query
        :return: String query
        """
        for param in params:
            assert ';' not in param
        final = query % (params)
        return final

    def update_game_state(self, game_id, game_state):
        """
        Update database entry for a given game - create new row if this doesn't already exist
        :param game_id: uuid for this game
        :param game_state: dictionary with game state information
        :return: Result of query
        """
        # TODO search for game_id / update if exits

        # Game not found - create new entry
        query = "INSERT INTO games (game_id, game_state) VALUES (%s, %s);"
        query = self.build_query(query, game_id, game_state)

        result = self.execute_query(query)

        return result

if __name__ == "__main__":
    # Testing database queries
    db = Database()
    params = ("\"asfasf-2325-fsaafa\"", "\"{'1':'x'}\"")
    query = db.build_query("INSERT INTO games (game_id, game_state) VALUES (%s, %s);", params[0], params[1])
    print db.execute_query(query)
