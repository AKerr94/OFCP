__author__ = 'Alastair Kerr'

from card import Card


class Player(object):
    def __init__(self, playerNumber=1, score=0, cards=[]):
        """
        Initialise player object
        Each player has a player number, a score and a Placement object with a top, middle and bottom row
        :return: None
        """
        assert isinstance(playerNumber, int)
        assert 1 <= playerNumber <= 4
        assert isinstance(score, int)
        for c in cards:
            assert isinstance(c, Card)

        self.playerNumber = playerNumber
        self.score = score
        self.scoresList = None # This is used to store information about a player's row scores on the current round
                               # List [Bool fouled, tuple bottom row score, tuple middle row score, tuple top row score]
        self.cards = cards     # Holds card objects player has been dealt so far this round
