__author__ = 'Alastair Kerr'

from placement import Placement
from deck import Deck


class Board():
    def __init__(self, playerCount=2):
        """
        Initialise board object composed of Player objects for each player and a Deck object
        :return: None
        """
        assert isinstance(playerCount, int)
        assert 2 <= playerCount <= 4

        self.playerCount = playerCount
        self.deck = Deck()

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
