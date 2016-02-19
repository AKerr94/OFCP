__author__ = 'Alastair Kerr'

from player import Player
from board import Board
from scorer import Scorer


class Game(object):
    def __init__(self, playerCount=2, firstToAct=1, deck=None, deckPosition=0):
        """
        Initialise Game object
        Each game has a current round number, Player objects and a board object for each round
        :param playerCount: int number of players
        :param firstToAct: int playerNumber who acts first this round
        :param deck: 104 char string containing card names format <rank><suit>*52
        :return: None
        """
        assert isinstance(playerCount, int)
        assert 2 <= playerCount <= 4
        assert isinstance(firstToAct, int)
        assert 1 <= firstToAct <= 4

        self.playerCount = playerCount
        self.firstToAct = firstToAct
        self.nextToAct = firstToAct
        self.actingOrder = self.generateActingOrder(firstToAct=firstToAct)
        self.actingOrderPointer = 0
        self.roundNumber = 1
        self.board = Board(playerCount=playerCount, deck=deck, deckPosition=deckPosition)

        self.player1 = Player(playerNumber=1)
        self.player2 = Player(playerNumber=2)
        self.player3 = None
        self.player4 = None
        if self.playerCount >= 3:
            self.player3 = Player(playerNumber=3)
        if self.playerCount == 4:
            self.player4 = Player(playerNumber=4)

        self.players = []
        for p in [self.player1, self.player2, self.player3, self.player4]:
            if (p != None):
                self.players.append(p)

        self.scoring = Scorer(players=self.players, board=self.board)

    def resetBoard(self):
        """
        Clears board and generates new deck of cards
        :return: None
        """
        self.board = Board(playerCount=self.playerCount)

    def newRound(self):
        """
        Start a new round
        :return: None
        """
        self.scoreAll()
        self.resetBoard()
        self.roundNumber += 1
        self.incrementNextToAct()
        self.actingOrder = self.generateActingOrder(self, self.nextToAct)

    def scoreBoard(self):
        """
        Scores the board
        :return: None
        """
        self.scoring.scoreAll()

    def generateActingOrder(self, firstToAct=1):
        """
        Generates actingOrder for clockwise rotation of player action
        :param firstToAct: int first player number to act
        :return: List actingOrder [first playerNumber, second playerNumber ..]
        """
        assert isinstance(firstToAct, int)
        assert 1 <= firstToAct <= self.playerCount

        actingOrder = []
        for i in range(firstToAct, self.playerCount + 1):
            actingOrder.append(i)

        for i in range(1, firstToAct):
            actingOrder.append(i)

        return actingOrder

    def incrementNextToAct(self):
        """
        Increments nextToAct var - if last player has acted, go back to first player for next round of placements
        :return: None
        """
        if (self.nextToAct == self.actingOrder[self.playerCount - 1]):
            self.actingOrderPointer = 0
            self.nextToAct = self.actingOrder[0]
        else:
            self.actingOrderPointer += 1
            self.nextToAct = self.actingOrder[self.actingOrderPointer]

    def dealFirstHand(self, playerNumber=1):
        """
        Deal 5 cards to the given player
        :param playerNumber: int playerNumber
        :return: 5 card objects
        """
        assert isinstance(playerNumber, int)
        assert 1 < playerNumber <= self.playerCount

        if (len(self.players[playerNumber - 1].cards) > 0):
            raise ValueError("Player already has cards dealt!")
        cards = self.board.deck.deal_n(5)
        self.players[playerNumber - 1].cards = cards
        return cards


if __name__ == "__main__":
    # Testing functionality
    for i in range(0,1):
        g = Game(playerCount=4, firstToAct=2)
        print("Order of player action: %s\n" % g.actingOrder)
        g.board.randomlyPopulateBoard()
        g.scoreBoard()
        for msg in g.scoring.scoresMessages:
            print(msg)
        print ""
        for p in g.players:
            print("Player %i's total score after this round = %i" % (p.playerNumber, p.score))
