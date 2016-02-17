__author__ = 'Alastair Kerr'

from player import Player
from board import Board


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

    def scoreAll(self):
        """
        Score every player's hand and modify their scores accordingly
        Naive method for now simply adding player's positive scores; TBD implement proper scoring system
        :return: None
        """
        for p in self.players:
            print("Scoring player %i") % p.playerNumber
            placements = self.board.placements[p.playerNumber -1]
            topRowScores = placements.topRow.scoreAndClassify()
            middleRowScores = placements.middleRow.scoreAndClassify()
            bottomRowScores = placements.bottomRow.scoreAndClassify()
            print("%s\n%s\n%s") % (topRowScores, middleRowScores, bottomRowScores)
            if bottomRowScores[1] >= middleRowScores[1] >= topRowScores[1]:
                print("OK\n")
            else:
                print("FOUL\n")


if __name__ == "__main__":
    # Testing functionality
    g = Game(playerCount=4)
    g.board.randomlyPopulateBoard()
    g.scoreAll()
