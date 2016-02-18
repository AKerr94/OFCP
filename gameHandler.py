__author__ = 'Alastair Kerr'

from ofc import OFC
from pineapple import Pineapple


class GameHandler(object):
    def __init__(self, variant='ofc', playerCount=2, gameState={}):
        """
        Initialises game handler object
        Game handler communicates between server and back end logic
        :return: None
        """
        assert isinstance(variant, basestring)
        assert variant.lower() in ['ofc', 'pineapple']
        assert isinstance(playerCount, int)
        assert 1 < playerCount <= 4
        assert isinstance(gameState, dict)

        self.game = None
        if (variant.lower() == 'ofc'):
            self.game = OFC(playerCount=playerCount)
        elif (variant.lower() == 'pineapple'):
            self.game = Pineapple(playerCount=playerCount)

        self.gameState = gameState
        if (self.gameState != {}):
            self.interpretGameStateJson()

    def interpretGameStateJson(self):
        """
        Interprets the JSON from gameState and updates the game objects with this information
        :return: None
        """
        pass

if __name__ == "__main__":
    # Testing functionality
    g = GameHandler(variant='ofc')
