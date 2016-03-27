__author__ = 'Alastair Kerr'

from row import Row
from card import Card


class Placement(object):
    def __init__(self, playerNumber=1):
        """
        Initialise placement - object with a top, middle and bottom row
        :return: None
        """
        assert isinstance(playerNumber, int)
        assert 1 <= playerNumber <= 4

        self.playerNumber = playerNumber
        self.bottomRow = Row(size=5, rowName='Bottom', playerNumber=playerNumber)
        self.middleRow = Row(size=5, rowName='Middle', playerNumber=playerNumber)
        self.topRow = Row(size=3, rowName='Top', playerNumber=playerNumber)

    def setRow(self, row='Bottom', cards=[]):
        """
        Sets a given row with cards provided
        :param cards: List of Card objects
        :return: None
        """
        assert isinstance(row, basestring)
        assert row.lower() in ['bottom', 'middle', 'top']
        assert isinstance(cards, list)
        if row.lower() in ['bottom', 'middle']:
            assert len(cards) <= 5
        elif row.lower() == 'top':
            assert len(cards) <= 3

        for i in range(1, len(cards) + 1):
            assert isinstance(cards[i-1], Card)

            if (row.lower() == 'bottom'):
                self.bottomRow.setPlacement(c=cards[i-1], position=i)

            elif (row.lower() == 'middle'):
                self.middleRow.setPlacement(c=cards[i-1], position=i)

            else:
                self.topRow.setPlacement(c=cards[i-1], position=i)
