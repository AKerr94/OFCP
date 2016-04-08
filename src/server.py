__author__ = 'Alastair Kerr'

import cherrypy
import json
import uuid
from datetime import datetime

import config
import tools
from gameHandler import GameHandler
from database_handler import Database


class api(object):
    """
    Application layer handling requests from frontend and responses from backend
    """
    def __init__(self):
        """
        Initialise required objects
        """
        self.db = Database()

    def make_game(self, playerCount=2, variant='ofc'):
        """
        Create a new game of the desired variant for the given amount of players
        :return: None, redirect to game page
        """
        assert variant in ['ofc', 'pineapple']
        maxPlayers = 4
        if variant == 'pineapple':
            maxPlayers = 3
        assert 2 <= playerCount <= maxPlayers

        game_id = uuid.uuid4()
        gameHandler = GameHandler(variant=variant, playerCount=playerCount)

        # Create database entry here with game state and game id
        game_state = gameHandler.getCompiledGameState()
        db_result = self.db.update_game_state("\"%s\"" % str(game_id), str(game_state))
        if db_result:
            raise cherrypy.HTTPError(500, "Database error! See error logs for dump.")

        raise cherrypy.HTTPRedirect("/render_game/%s" % game_id)

    def render_game(self, game_id=None):
        """
        Returns page from template using game state information for the provided game id
        :param game_id: uuid4 format id for this game
        :return: HTML rendered from template
        """
        if (game_id == None):
            raise cherrypy.HTTPError(500, "No game id was provided for this request!")

        game_state = self.db.query_by_game_id(game_id, 'game_state')
        print game_state

        # TODO render template and return

    def ofc_backend(self, **params):
        """
        Handles interaction between frontend and backend - interprets game state information from POSTed JSON with game id
        :param params: Expected: game_id, game_state
        :return: Next action information (e.g. player number + cards to place)
        """
        try:
            game_state = json.loads(params['game_state'])
            game_id = params['game_id']
        except:
            with open('%s/error_logs' % config.LOGS_DIR, 'a') as f:
                f.write("%s: ofc_backend failed to interpret request: %s\n" % (tools.get_formatted_datetime(), params))
            raise cherrypy.HTTPError(500, "Invalid request! See error logs for dump.")

        # TODO Generate response


    make_game.exposed = True
    render_game.exposed = True
    ofc_backend.exposed = True


if __name__ == "__main__":
    cherrypy.quickstart(api(), '/', config.cherrypy_config)
