# Author: Alastair Kerr

from row import Row


class Player():
    def __init__(self, playerNumber=1, score=0):
        """
        Initialise player object
        Each player has a top, middle and bottom row of cards, a player number, and a score
        :return: None
        """
        assert isinstance(playerNumber, int)
        assert 1 <= playerNumber <= 4
        assert isinstance(score, int)

        self.playerNumber = playerNumber
        self.score = score
        self.bottomRow = Row(size=5, rowName='Bottom', playerNumber=self.playerNumber)
        self.middleRow = Row(size=5, rowName='Middle', playerNumber=self.playerNumber)
        self.topRow = Row(size=3, rowName='Top', playerNumber=self.playerNumber)
