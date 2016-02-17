__author__ = 'Alastair Kerr'

from player import Player
from board import Board
from scorer import Scorer


class Game():
    def __init__(self, playerCount=2):
        """
        Initialise Game object
        Each game has a current round number, Player objects and a board object for each round
        :return: None
        """
        assert isinstance(playerCount, int)
        assert 2 <= playerCount <= 4

        self.playerCount = playerCount
        self.roundNumber = 1
        self.board = Board(playerCount=playerCount)

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

    def scoreBoard(self):
        """
        Scores the board
        :return: None
        """
        scoring = Scorer(players=self.players, board=self.board)
        scoring.scoreAll()



if __name__ == "__main__":
    # Testing functionality
    for i in range(0,1):
        g = Game(playerCount=4)
        g.board.randomlyPopulateBoard()
        g.scoreBoard()
