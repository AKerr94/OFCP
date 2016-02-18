__author__ = 'Alastair Kerr'

from row import Row


class Placement(object):
    def __init__(self, playerNumber=1):
        """
        Initialise placement - object with a top, middle and bottom row
        :return: None
        """
        self.playerNumber = playerNumber
        self.bottomRow = Row(size=5, rowName='Bottom', playerNumber=playerNumber)
        self.middleRow = Row(size=5, rowName='Middle', playerNumber=playerNumber)
        self.topRow = Row(size=3, rowName='Top', playerNumber=playerNumber)
