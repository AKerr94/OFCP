__author__ = 'Alastair Kerr'

from game import Game


class Pineapple(Game):
    """
    Pineapple variant of the game
    """

    def __init__(self, playerCount=2, firstToAct=1, nextToAct=1, actingOrderPointer=0, roundNumber=1, \
                 variant='pineapple', roundActionNumber=1, deck=None, deckPointer=0):
        """
        Initialise - pineapple can be played with max 3 players. If this is OK call super constructor
        :return: None
        """
        if (playerCount > 3):
            raise ValueError("Pineapple OFCP can have a maximum of 3 players!")
        super(Pineapple, self).__init__(playerCount=self.playerCount, firstToAct=firstToAct, nextToAct=nextToAct, \
                            actingOrderPointer=actingOrderPointer, roundNumber=roundNumber, roundActionNumber=roundActionNumber, \
                            deck=deck, deckPointer=deckPointer,variant='pineapple')

    # TODO pineapple ofc specific game logic functions/ implementation


if __name__ == "__main__":
    # Testing functionality
    g = Pineapple(playerCount=3)
