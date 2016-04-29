__author__ = 'Alastair Kerr'

from player import Player
from board import Board
from scorer import Scorer
import tools


class Game(object):
    def __init__(self, playerCount=2, firstToAct=1, nextToAct=1, actingOrderPointer=0, \
                 roundNumber=1, roundActionNumber=1, deck=None, deckPointer=0, variant='ofc'):
        """
        Initialise Game object
        Each game has a current round number, Player objects and a board object for each round
        :param playerCount: int number of players
        :param firstToAct: int playerNumber who acts first this round
        :param deck: 104 char string containing card names format <rank><suit>*52
        :return: None
        """
        assert isinstance(playerCount, int)
        assert 2 <= playerCount <= 4
        assert isinstance(firstToAct, int)
        assert 1 <= firstToAct <= 4

        self.playerCount = playerCount
        self.firstToAct = firstToAct
        self.nextToAct = nextToAct
        self.actingOrder = self.generateActingOrder(firstToAct=firstToAct)
        self.actingOrderPointer = actingOrderPointer
        self.roundActionNumber = roundActionNumber
        self.roundNumber = roundNumber
        self.variant = variant

        self.board = Board(playerCount=playerCount, deck=deck, deckPointer=deckPointer)
        self.players = self.createPlayers()

        self.scoring = Scorer(players=self.players, board=self.board)

    def createPlayers(self):
        """
        Used to initialise the player objects based on given player requirements
        :return: List of player objects in ascending numerical order
        """
        player1 = Player(playerNumber=1)
        player2 = Player(playerNumber=2)
        player3 = None
        player4 = None
        if self.playerCount >= 3:
            player3 = Player(playerNumber=3)
        if self.playerCount == 4:
            player4 = Player(playerNumber=4)

        players = []
        for p in [player1, player2, player3, player4]:
            if (p != None):
                players.append(p)

        return players

    def resetBoard(self):
        """
        Clears board and generates new deck of cards
        :return: None
        """
        self.board = Board(playerCount=self.playerCount)

    def newRound(self):
        """
        Start a new round
        :return: None
        """
        self.scoreAll()
        self.resetBoard()
        self.roundNumber += 1
        self.incrementNextToAct()
        self.actingOrder = self.generateActingOrder(self, self.nextToAct)

    def scoreBoard(self):
        """
        Scores the board
        :return: None
        """
        self.scoring.scoreAll()

    def interpretScores(self):
        """
        Calls and interprets results of scorer
        :return: string scores interpretation
        """
        self.scoreBoard()
        returnStr = ""
        for message in self.scoring.scoresMessages:
            returnStr += message + "\n"
        returnStr += "\n"
        for player in self.players:
            returnStr += "Player %i's total score after this round = %i\n" % \
                         (player.playerNumber, player.score)
        return returnStr

    def generateActingOrder(self, firstToAct=1):
        """
        Generates actingOrder for clockwise rotation of player action
        :param firstToAct: int first player number to act
        :return: List actingOrder [first playerNumber, second playerNumber ..]
        """
        assert isinstance(firstToAct, int)
        assert 1 <= firstToAct <= self.playerCount

        actingOrder = []
        for i in range(firstToAct, self.playerCount + 1):
            actingOrder.append(i)

        for i in range(1, firstToAct):
            actingOrder.append(i)

        return actingOrder

    def incrementNextToAct(self):
        """
        Increments nextToAct var and if necessary, the roundActionNumber
        If last player has acted, go back to first player for next round of placements
        :return: None
        """
        if (self.nextToAct == self.actingOrder[self.playerCount - 1]):
            self.actingOrderPointer = 0
            self.nextToAct = self.actingOrder[0]
            self.roundActionNumber += 1
        else:
            self.actingOrderPointer += 1
            self.nextToAct = self.actingOrder[self.actingOrderPointer]

    def handleNextAction(self):
        """
        Determines which method to call next and for which player
        If the last action has happened will pass request to scoring handler and return that response instead
        :return: [int playerNumber, int roundActionNumber, [Card card]]
        """
        playerNumber = self.nextToAct
        cardsDealt = []

        if (self.roundActionNumber == 1):
            cardsDealt = self.dealFirstHand(playerNumber)
        elif (self.roundActionNumber <= 9):
            cardsDealt = self.dealSubsequentRounds(playerNumber)
        else:
            tools.write_error("handleNextAction(): All action for this round has finished!")
            raise ValueError("All action for this round has finished!")

        return [playerNumber, self.roundActionNumber, cardsDealt]

    def dealFirstHand(self, playerNumber):
        """
        Deal 5 cards to the given player
        :param playerNumber: int playerNumber
        :return: [5 card objects]
        """
        assert self.roundActionNumber == 1
        assert isinstance(playerNumber, int)
        assert 1 <= playerNumber <= self.playerCount

        if (len(self.players[playerNumber - 1].cards) > 0):
            raise ValueError("Player already has cards dealt!")
        cards = self.board.deck.deal_n(5)
        self.players[playerNumber - 1].cards = cards
        self.incrementNextToAct()

        return cards

    def dealSubsequentRounds(self, playerNumber):
        """
        Deal one card to the given player
        :param playerNumber: int playerNumber
        :return: [1 card object]
        """
        assert self.roundActionNumber > 1
        assert isinstance(playerNumber, int)
        assert 1 <= playerNumber <= self.playerCount

        card = self.board.deck.deal_one()
        self.players[playerNumber - 1].cards.append(card)
        self.incrementNextToAct()

        return [card]


if __name__ == "__main__":
    # Testing functionality - randomly populating board using game action logic
    playerCount = 4
    for gameCount in range(0,1):
        g = Game(playerCount=playerCount, firstToAct=1)
        print("Order of player action: %s\n" % g.actingOrder)
        cardLists = []

        for i in range(0, playerCount):
            cardLists.append([])

        for i in range(0,9):
            for j in range(1, playerCount+1):
                action = g.handleNextAction()
                player = action[0]
                cards = action[2]
                for card in cards:
                    cardLists[player-1].append(card)

        for i in range(1, playerCount+1):
            g.board.placements[i-1].setRow(row='Bottom', cards=cardLists[i-1][0:5])
            g.board.placements[i-1].setRow(row='Middle', cards=cardLists[i-1][5:10])
            g.board.placements[i-1].setRow(row='Top', cards=cardLists[i-1][10:13])
        print(g.interpretScores())
