# Author: Alastair Kerr

from player import Player
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
        self.player1 = Player(playerNumber=1)
        self.player2 = Player(playerNumber=2)
        self.player3 = None
        self.player4 = None
        if self.playerCount >= 3:
            self.player3 = Player(playerNumber=3)
        if self.playerCount == 4:
            self.player4 = Player(playerNumber=4)

        self.deck = Deck()

if __name__ == '__main__':
    # Testing functionality
    b = Board(playerCount=3)
    cards = b.deck.deal_n(5)
    for i in range(0,5):
        b.player3.middleRow.setPlacement(c=cards[i], position=i+1)
    print "Hand `%s` classified as `%s`" % (b.player3.middleRow.getPokerHand(), b.player3.middleRow.classifyRow())
