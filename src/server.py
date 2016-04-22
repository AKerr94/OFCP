__author__ = 'Alastair Kerr'

import cherrypy
import json
import uuid
from jinja2 import Environment, FileSystemLoader

import config
import tools
from gameHandler import GameHandler
from database_handler import Database

env = Environment(loader=FileSystemLoader('templates'))


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

        # Create database entry with game state and game id
        game_state = gameHandler.getCompiledGameState()
        db_result = self.db.update_game_state(str(game_id), str(game_state))
        if db_result:
            tools.write_error(db_result)
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

        game_state = self.db.get_game_state(game_id, sanitised=True)

        return render_template('game.html', game_id=game_id, game_state=game_state)

    def ofc_backend(self, **params):
        """
        Handles interaction between frontend and backend - interprets request in form of JSON from POST
        :param params: Expected: game_id, payload (details of request for backend)
        :return: Next action information (e.g. player number + cards to place)
        """
        try:
            payload = json.loads(params['payload'])
            assert 'action' in payload.keys()
            game_id = params['game_id']
            game_state = self.db.get_game_state(game_id)
        except:
            tools.write_error("ofc_backend failed to interpret request: %s\n" % params)
            raise cherrypy.HTTPError(500, "Invalid request! See error logs for dump.")

        game = GameHandler(variant=game_state['variant'], playerCount=game_state['playerCount'], gameState=game_state)
        if payload['action'] == 'nextAction':
            response = game.getNextActionDetails()
        else:
            tools.write_error("ofc_backend invalid payload action: '%s' with payload: '%s'\n" % (payload['action'], payload))
            raise cherrypy.HTTPError(500, "Invalid request! See error logs for dump.")

        return response

    make_game.exposed = True
    render_game.exposed = True
    ofc_backend.exposed = True


def render_template(template, **kwargs):
    """
    Returns HTML rendered from template with passed args
    :param template: Filename in templates/
    :param kwargs: Variables used in template
    :return: Rendered template
    """
    t = env.get_template(template)
    return t.render(**kwargs)

if __name__ == "__main__":
    cherrypy.quickstart(api(), '/', config.cherrypy_config)
