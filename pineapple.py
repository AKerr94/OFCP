__author__ = 'Alastair Kerr'

from game import Game


class Pineapple(Game):
    """
    Pineapple variant of the game
    """

    def __init__(self, playerCount=2, firstToAct=1, deck=None, deckPosition=0):
        """
        Initialise - pineapple can be played with max 3 players. If this is OK call super constructor
        :return: None
        """
        if (playerCount > 3):
            raise ValueError("Pineapple OFCP can have a maximum of 3 players!")
        super(Pineapple, self).__init__()


if __name__ == "__main__":
    # Testing functionality
    g = Pineapple(playerCount=3)
