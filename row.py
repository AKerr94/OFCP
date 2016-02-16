# Author: Alastair Kerr

import eval
from deck import Deck
from card import Card


class Row():
    def __init__(self, size=5, rowName='Bottom', playerNumber=1, cardPlacements=[]):
        """
        Initialise row of given size (3 or 5), rowName (Bottom, Middle or Top), playerNumber (1-4), and cards placed
        :return: None
        """
        assert size in [3, 5]
        assert rowName in ['Bottom', 'Middle', 'Top']
        assert isinstance(playerNumber, int)
        assert 1 <= playerNumber <= 4
        assert isinstance(cardPlacements, list)

        self.size = size
        self.rowName = rowName
        self.playerNumber = playerNumber
        self.pokerHand = ""

        self.cardPlacements = []
        # Use any supplied card placements or default to None value indicating empty slot
        for i in range(0, self.size):
            try:
                self.cardPlacements.append(cardPlacements[i])
            except:
                self.cardPlacements.append(None)

    def setPlacement(self, c=Card(), position=1):
        """
        Set a given position's card placement as the given card object
        :param c: Card object
        :param position: Int position (1 <= position <= row size)
        :return: None
        """
        assert isinstance(c, Card)
        assert isinstance(position, int)
        assert 1 <= position <= self.size

        self.cardPlacements[position -1] = c

    def getPokerHand(self):
        """
        Generates 10 char string containing details of poker hand in this row, stores as pokerHand
        :return: 10 char poker hand string
        """
        self.pokerHand = ""
        for c in self.cardPlacements:
            assert c != None
            self.pokerHand += c.name
        return self.pokerHand

    def scoreRow(self):
        """
        Get poker hand string and use hand evaluator to score it
        :return: Poker hand score
        """
        self.getPokerHand()
        return eval.score_5(self.pokerHand)

    def classifyRow(self):
        """
        Get poker hand string and return human readable classification
        :return: Poker hand class
        """
        self.getPokerHand()
        return eval.classify_5(self.pokerHand)

if __name__ == "__main__":
    # Testing functionality - initialise row with 5 random cards and classify this poker hand
    r = Row(rowName='Middle', playerNumber=2)

    d = Deck()
    for i in range(0, 5):
        r.setPlacement(d.deal_one(), i + 1)

    print r.getPokerHand()
    print r.classifyRow()
