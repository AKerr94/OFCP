__author__ = 'Alastair Kerr'

class Card(object):
    def __init__(self, card="AH"):
        """
        Initialise card
        :return: None
        """
        assert isinstance(card, basestring)
        assert len(card) == 2
        assert card[0].upper() in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        assert card[1].upper() in ['H', 'S', 'D', 'C']

        self.card = card
        self.rank = card[0]
        self.suit = card[1]
