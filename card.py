__author__ = 'Alastair Kerr'

class Card(object):
    def __init__(self, rank='A', suit='H'):
        """
        Initialise card
        :return: None
        """
        assert isinstance(rank, basestring)
        assert rank.upper() in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        assert isinstance(suit, basestring)
        assert suit.upper() in ['H', 'S', 'D', 'C']

        self.rank = rank
        self.suit = suit
        self.name = rank + suit
