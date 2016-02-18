__author__ = 'Alastair Kerr'

class Card(object):
    def __init__(self, rank='A', suit='H'):
        """
        Initialise card
        :return: None
        """
        assert isinstance(rank, basestring)
        assert len(rank) == 1
        assert isinstance(suit, basestring)
        assert len(suit) == 1

        self.rank = rank
        self.suit = suit
        self.name = rank + suit
