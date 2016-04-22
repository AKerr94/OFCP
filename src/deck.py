__author__ = 'Alastair Kerr'

import random

from card import Card


class Deck (object):
    def __init__(self, shuffled=True, currentPosition=0, deck=None):
        """
        Initialise deck object with 52 cards
        :param shuffled: If true, shuffles initialised deck
        :param currentPosition: Current position in deck to deal from
        :return: None
        """
        assert isinstance(shuffled, bool)
        assert isinstance(currentPosition, int)

        ranks = ['2', '3' ,'4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['H', 'D', 'S', 'C']
        self.deck = []
        self.currentPosition = currentPosition

        if (deck == None):
            for suit in suits:
                for rank in ranks:
                    c = Card(card=rank+suit)
                    self.deck.append(c)

            if (shuffled):
                self.deck = self.shuffle(self.deck)

        else:
            assert isinstance(deck, list)
            assert len(deck) == 52
            for card in deck:
                if type(card) == Card:
                    self.deck.append(card)
                else:
                    assert isinstance(card, basestring)
                    assert len(card) == 2
                    self.deck.append(Card(card))

    def shuffle(self, cards):
        """
        :param cards: Deck object
        :return: Shuffled deck
        """
        assert isinstance(cards, list)

        random.shuffle(cards)
        return cards

    def deal_one(self):
        """
        Deal a card
        :return: Card object
        """
        self.currentPosition += 1
        if (self.currentPosition > 52):
            raise ValueError("Run out of cards in the deck!")
        return self.deck[self.currentPosition -1]

    def deal_n(self, n):
        """
        Calls deal_one n times
        :param n: Number of cards to deal
        :return: List of Card objects
        """
        assert isinstance(n, int)

        return [self.deal_one() for i in range(0, n)]

if __name__ == "__main__":
    # Testing functionality
    d = Deck(deck="7C9C6C3S5S5D3C8HQHQCAHTSKD5C4H7DACJS7S9SADKS6STH4DQS6D7H8D5H4C8S4SJC3HAS3D8C6H2SKCQDTD9H9DJDKHTC2D2C2HJH")
    for i in range(0,52):
        print(d.deal_one().card)
