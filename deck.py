__author__ = 'Alastair Kerr'

import random

from card import Card


class Deck (object):
    def __init__(self, shuffled=True, currentPosition=0):
        """
        Initialise deck object with 52 cards
        :param shuffled: If true, shuffles initialised deck
        :param currentPosition: Current position in deck to deal from
        :return: None
        """
        assert isinstance(shuffled, bool)
        assert isinstance(currentPosition, int)

        self.deck = []
        self.currentPosition = currentPosition

        ranks = ['2', '3' ,'4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['H', 'D', 'S', 'C']
        for suit in suits:
            for rank in ranks:
                c = Card(rank, suit)
                self.deck.append(c)

        if (shuffled):
            self.deck = self.shuffle(self.deck)

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
    d = Deck()
    for i in range(0,52):
        print(d.deal_one().name)
