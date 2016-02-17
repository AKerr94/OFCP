__author__ = 'Alastair Kerr'

import eval, eval3c
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
        for c in cardPlacements:
            assert isinstance(c, Card)

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

    def setPlacement(self, c=Card(), position=1, force=False):
        """
        Set a given position's card placement as the given card object
        :param c: Card object
        :param position: Int position (1 <= position <= row size)
        :return: None
        """
        assert isinstance(c, Card)
        assert isinstance(position, int)
        assert 1 <= position <= self.size

        if (self.cardPlacements[position -1] == None or force):
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
        if (self.size == 3):
            return eval3c.score_3(self.pokerHand)
        elif (self.size == 5):
            return eval.score_5(self.pokerHand)

    def classifyRow(self):
        """
        Get poker hand string and return human readable classification
        :return: Poker hand class
        """
        self.getPokerHand()
        if (self.size == 3):
            return eval3c.classify_3(self.pokerHand)
        elif (self.size == 5):
            return eval.classify_5(self.pokerHand)

    def scoreAndClassify(self):
        """
        Function to score and classify this row's poker hand
        :return: List [pokerHand, score, classification]
        """
        self.getPokerHand()
        score = self.scoreRow()
        classification = self.classifyRow()
        return [self.pokerHand, score, classification]


if __name__ == "__main__":
    # Testing functionality - initialise row with 5 random cards and classify this poker hand
    r = Row(rowName='Middle', playerNumber=2)

    d = Deck()
    for i in range(0, 5):
        r.setPlacement(d.deal_one(), i + 1)

    print r.getPokerHand()
    print r.classifyRow()
