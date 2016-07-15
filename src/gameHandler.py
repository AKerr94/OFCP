__author__ = 'Alastair Kerr'

import json

from ofc import OFC
from pineapple import Pineapple
import gameHandlerHelpers


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

        self.playerCount = playerCount
        self.gameState = gameState

        # Set defaults - overridden if gameState is passed
        firstToAct, nextToAct, actingOrderPointer, roundNumber, roundActionNumber, deck, deckPointer = 1, 1, 0, 1, 1, None, 0

        if (gameState != {}):
            # Game state info overrides existing variables e.g. playerCount
            self.interpretPlayerCount(gameState)
            firstToAct, nextToAct, actingOrderPointer, roundNumber, roundActionNumber, deck, deckPointer = \
                self.interpretGameVars(gameState['gameState'])

        self.game = None
        # Create a game object for the desired variant using any read in variables
        if (variant.lower() == 'ofc'):
            self.game = OFC(playerCount=self.playerCount, firstToAct=firstToAct, nextToAct=nextToAct, \
                            actingOrderPointer=actingOrderPointer, roundNumber=roundNumber, variant='ofc', \
                            roundActionNumber=roundActionNumber, deck=deck, deckPointer=deckPointer)

        elif (variant.lower() == 'pineapple'):
            self.game = Pineapple(playerCount=self.playerCount, firstToAct=firstToAct, nextToAct=nextToAct, \
                            actingOrderPointer=actingOrderPointer, roundNumber=roundNumber, variant='pineapple', \
                            roundActionNumber=roundActionNumber, deck=deck, deckPointer=deckPointer)

        if (gameState != {}):
            # Update game state objects with read in information
            self.interpretGameStatePlacements(gameState)
            self.interpretPlayerCards(gameState)

    def interpretPlayerCount(self, gameState={}):
        """
        Reads game state playerNumber to work out how many player objects to initialise the game object with
        :param gameState: dict game state
        :return: None
        """
        assert isinstance(gameState, dict)
        assert 'playerCount' in gameState.keys()
        self.playerCount = gameState['playerCount']
        assert isinstance(self.playerCount, int)
        assert 1 < self.playerCount <= 4

    def interpretPlayerCards(self, gameState={}):
        """
        Interprets player cards from game state and updates game objects
        :param gameState: Game State dict
        :return: None
        """
        assert isinstance(gameState, dict)
        for i in range(1, self.playerCount+1):
            self.game.players[i-1].cards = gameHandlerHelpers.convertCardsListToObj(gameState['players'][str(i)]['cards'])

    def interpretGameVars(self, gameState={}):
        """
        Interprets game and round variables and returns these to initialise game objects with
        :param gameState: 'gameState' key:dict
        :return: firstToAct, nextToAct, actingOrderPointer, roundNumber, roundActionNumber, deck, deckPointer
        """
        firstToAct = gameState['firstToAct']
        nextToAct = gameState['nextToAct']
        actingOrderPointer = gameState['actingOrderPointer']
        roundNumber = gameState['roundNumber']
        roundActionNumber = gameState['roundActionNumber']
        deck = gameState['deck']
        deckPointer = gameState['deckPointer']

        return firstToAct, nextToAct, actingOrderPointer, roundNumber, roundActionNumber, deck, deckPointer

    def interpretGameStatePlacements(self, gameState={}):
        """
        Interprets the gameState placements and updates the game objects with this information
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
                                   bottomRowCards=gameHandlerHelpers.convertCardsListToObj(placementsDic[key]['bottomRow']), \
                                   middleRowCards=gameHandlerHelpers.convertCardsListToObj(placementsDic[key]['middleRow']), \
                                   topRowCards=gameHandlerHelpers.convertCardsListToObj(placementsDic[key]['topRow']))

    def getCompiledGameState(self):
        """
        Returns the compile JSON game state for the game object associated with this handler instance
        :return: Game state JSON
        """
        return gameHandlerHelpers.compileGameState(self.game)

    def getNextActionDetails(self):
        """
        Calls game object to determine next action
        :return: [Player number, round action number, [cards to place]]
        """
        payload = self.game.handleNextAction()
        payload[2] = gameHandlerHelpers.convertCardsListToStr(payload[2])
        return gameHandlerHelpers.formatNextActionResponse(payload)

    def rowPlacementsAreIdentical(self, new_game_state, playerNumber, rowName):
        """
        Determines if the placements for a given row are the same in a given game state compared to that of the game state from the previous action
        Used as a supplementary function called by playerGameStateIsIdentical
        :param new_game_state: Dictionary game state
        :param playerNumber: Int/ str player number
        :param rowName: Str bottom, middle or top
        :return: True - Placements are identical, False - inconsistent placements
        """
        assert 0 < int(playerNumber) <= self.playerCount
        playerNumber = str(playerNumber)
        rowName = rowName.lower()
        assert rowName in ['bottom', 'middle', 'top']

        row = "%sRow" % rowName
        oldPlacement = self.gameState['gameState']['placements'][playerNumber][row]
        newPlacement = new_game_state['gameState']['placements'][playerNumber][row]

        if oldPlacement != newPlacement:
            return False
        return True

    def playerGameStateIsIdentical(self, new_game_state, playerNumber):
        """
        Determines if the game state information for the given player is identical in the new game state to the game state from the previous action
        Used to validate that no other changes were made, except for those by the player whose turn it was to act
        :param new_game_state: Dictionary game state
        :param playerNumber: Int/ str player number
        :return: True - no erroneous changes, False - inconsistent game states
        """
        assert 0 < int(playerNumber) <= self.playerCount
        playerNumber = str(playerNumber)

        playerScoreOld = self.gameState['players'][playerNumber]['score']
        playerScoreNew = new_game_state['players'][playerNumber]['score']
        if playerScoreOld != playerScoreNew:
            return False

        playerCardsOld = self.gameState['players'][playerNumber]['cards']
        playerCardsNew = new_game_state['players'][playerNumber]['cards']
        if playerCardsOld != playerCardsNew:
            return False

        for row in ['bottom', 'middle', 'top']:
            if self.rowPlacementsAreIdentical(new_game_state, playerNumber, row) != True:
                return False

        return True

    def validateNewPlacements(self, new_game_state):
        """
        Validates new game state against current game state to ensure legitimate moves were made
        Validate that no other agents game state information has changed except the agent whose turn it was to act
        Validate that changes to the agent whose turn it was to act were legitimate
        :param game_state: New game state
        :return: True/ False
        """
        lastActor = self.game.actingOrder[self.game.actingOrderPointer]
        
        # Validate no other player's game state has changed 
        for playerNumber in [x for x in self.game.actingOrder if x != lastActor]:
            if self.playerGameStateIsIdentical(new_game_state, playerNumber) != True:
                return False

        # TODO validate last actor's changes are legitimate

        return True

    def updateGameState(self, game_state):
        """
        Updates this object's game state with new values from param game_state
        :param game_state: New game state
        :return: None
        """
        self.game.roundNumber = int(game_state['gameState']['roundNumber'])
        self.game.roundActionNumber = int(game_state['gameState']['roundActionNumber'])
        self.game.firstToAct = int(game_state['gameState']['firstToAct'])
        self.game.nextToAct = int(game_state['gameState']['nextToAct'])
        self.game.actingOrderPointer = int(game_state['gameState']['actingOrderPointer'])
        self.game.board.deck.currentPosition = int(game_state['gameState']['deckPointer'])

        for playerNumber in game_state['players'].keys():
            self.game.players[int(playerNumber)-1].cards = gameHandlerHelpers.convertCardsListToObj(game_state['players'][playerNumber]['cards'])
            self.game.players[int(playerNumber)-1].score = int(game_state['players'][playerNumber]['score'])
            self.game.board.placements[int(playerNumber)-1].bottomRow.cardPlacements = \
                gameHandlerHelpers.convertCardsListToObj(game_state['gameState']['placements'][playerNumber]['bottomRow'])
            self.game.board.placements[int(playerNumber)-1].middleRow.cardPlacements = \
                gameHandlerHelpers.convertCardsListToObj(game_state['gameState']['placements'][playerNumber]['middleRow'])
            self.game.board.placements[int(playerNumber)-1].topRow.cardPlacements = \
                gameHandlerHelpers.convertCardsListToObj(game_state['gameState']['placements'][playerNumber]['topRow'])

        return "Successfully updated game state!"


if __name__ == "__main__":
    # Testing functionality
    jsonFile = json.load(open("json_test"))
    g = GameHandler(variant='ofc', gameState=jsonFile)
    pNum = 1
    # Board object setPlacements method sets placements in an array, index[0] -> player 1, index[1] -> player 2 ...
    for p in g.game.board.placements:
        print "Player %s: Bottom %s (%s), middle %s (%s), top %s (%s)" % \
              (pNum, p.bottomRow.humanReadable(), p.bottomRow.classifyRow(), \
               p.middleRow.humanReadable(), p.middleRow.classifyRow(), \
               p.topRow.humanReadable(), p.topRow.classifyRow() )
        pNum += 1
    print "\nNow interpreting scores for this game state...\n"
    print g.game.interpretScores()
    print g.getCompiledGameState()
