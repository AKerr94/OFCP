__author__ = 'Alastair Kerr'

from placement import Placement
from deck import Deck
from card import Card


class Board(object):
    def __init__(self, playerCount=2, deck=None):
        """
        Initialise board object composed of Player objects for each player and a Deck object
        :return: None
        """
        assert isinstance(playerCount, int)
        assert 2 <= playerCount <= 4

        self.playerCount = playerCount
        self.deck = Deck(deck=deck)

        self.player1placements = Placement(playerNumber=1)
        self.player2placements = Placement(playerNumber=2)
        self.player3placements = None
        self.player4placements = None
        if (playerCount >= 3):
            self.player3placements = Placement(playerNumber=3)
        if (playerCount == 4):
            self.player4placements = Placement(playerNumber=4)

        self.placements = []
        for p in [self.player1placements, self.player2placements, self.player3placements, self.player4placements]:
            if (p != None):
                self.placements.append(p)

    def setPlacement(self, playerNumber=1, bottomRowCards=[], middleRowCards=[], topRowCards=[]):
        """
        Used to set card placements for given player
        :param playerNumber: int 1-4
        :param bottomRowCards: List of Card objects
        :param middleRowCards: List of Card objects
        :param topRowCards: List of Card objects
        :return: None
        """
        assert isinstance(playerNumber, int)
        assert 1 < playerNumber <= 4
        for row in [bottomRowCards, middleRowCards, topRowCards]:
            assert isinstance(row, list)
            assert len(row) <= 5
            for card in row:
                assert isinstance(card, Card)

        self.placements[playerNumber - 1].setRow(row='Bottom', cards=bottomRowCards)
        self.placements[playerNumber - 1].setRow(row='Middle', cards=middleRowCards)
        self.placements[playerNumber - 1].setRow(row='Top', cards=topRowCards)


    def randomlyPopulateBoard(self):
        """
        Randomly populate each player's placements with cards from deck
        Useful for simulations/ testing purposes
        :return: None
        """
        for placement in self.placements:
            cards = self.deck.deal_n(13)
            topRow = placement.topRow
            for i in range(1, 4):
                topRow.setPlacement(c=cards.pop(), position=i)
            middleRow = placement.middleRow
            for i in range(1, 6):
                middleRow.setPlacement(c=cards.pop(), position=i)
            bottomRow = placement.bottomRow
            for i in range(1, 6):
                bottomRow.setPlacement(c=cards.pop(), position=i)


if __name__ == '__main__':
    # Testing functionality
    b = Board(playerCount=3)
    testRow = b.player3placements.middleRow
    cards = b.deck.deal_n(5)
    for i in range(0,5):
        testRow.setPlacement(c=cards[i], position=i+1)
    print "Hand `%s` classified as `%s`" % (testRow.getPokerHand(), testRow.classifyRow())
