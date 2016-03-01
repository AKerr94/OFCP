__author__ = 'Alastair Kerr'

from placement import Placement
from deck import Deck
from card import Card


class Board(object):
    def __init__(self, playerCount=2, deck=None, deckPointer=0):
        """
        Initialise board object composed of Player objects for each player and a Deck object
        :return: None
        """
        assert isinstance(playerCount, int)
        assert 2 <= playerCount <= 4

        self.playerCount = playerCount
        self.deck = Deck(deck=deck, currentPosition=deckPointer)

        self.placements = self.initPlacements()

    def initPlacements(self):
        """
        Initialises the placement objects for this board (1 for each player)
        :return: List of placement objects
        """
        player1placements = Placement(playerNumber=1)
        player2placements = Placement(playerNumber=2)
        player3placements = None
        player4placements = None
        if (self.playerCount >= 3):
            player3placements = Placement(playerNumber=3)
        if (self.playerCount == 4):
            player4placements = Placement(playerNumber=4)

        placements = []
        for p in [player1placements, player2placements, player3placements, player4placements]:
            if (p != None):
                placements.append(p)

        return placements

    def setPlacements(self, playerNumber=1, bottomRowCards=[], middleRowCards=[], topRowCards=[]):
        """
        Used to set card placements for given player
        :param playerNumber: int 1-4
        :param bottomRowCards: List of Card objects
        :param middleRowCards: List of Card objects
        :param topRowCards: List of Card objects
        :return: None
        """
        assert isinstance(playerNumber, int)
        assert 1 <= playerNumber <= 4
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
