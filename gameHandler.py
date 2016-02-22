__author__ = 'Alastair Kerr'

import json

from ofc import OFC
from pineapple import Pineapple
from card import Card


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
        if (gameState != {}):
            self.interpretGameState(gameState)

    def interpretGameState(self, gameState={}):
        """
        Interprets the gameState and updates the game objects with this information
        :return: None
        """
        nestedPlacementsDict = gameState['gameState']['placements']
        for playerKey in nestedPlacementsDict.keys():
            self.interpretPlayerPlacements(nestedPlacementsDict, playerKey)

    def interpretPlayerPlacements(self, placementsDic, key):
        """
        Reads dictionary and interprets the placements and updates the game's board object with this information
        :param placementsDic: Gamestate dictionary at nested level ['gameState']['placements']
        :param key: The desired player whose placements are to be interpreted i.e. '1', '2', '3', '4'
        :return: None
        """
        assert isinstance(placementsDic, dict)
        assert isinstance(key, basestring)
        assert key in ['1', '2', '3', '4']
        self.game.board.setPlacements(playerNumber=int(key), \
                                   bottomRowCards=self.convertStringToCards(placementsDic[key]['bottomRow']), \
                                   middleRowCards=self.convertStringToCards(placementsDic[key]['middleRow']), \
                                   topRowCards=self.convertStringToCards(placementsDic[key]['topRow']))

    def convertStringToCards(self, rowString):
        """
        Takes in a row string e.g. "AHADKCKD8S" and converts it into a list of Card objects
        :param rowString String <rank><suit> * 3 or 5 cards
        :return: List of Card objects
        """
        assert isinstance(rowString, basestring)
        assert len(rowString) in [6, 10]
        rowList = []
        for i in xrange(0, len(rowString), 2):
            rowList.append(Card(rowString[i:i+2]))
        return rowList


if __name__ == "__main__":
    # Testing functionality
    jsonFile = json.load(open("json_test"))
    g = GameHandler(variant='ofc', gameState=jsonFile)
    for p in g.game.board.placements:
        print p.bottomRow.humanReadable(), p.middleRow.humanReadable(), p.topRow.humanReadable()
