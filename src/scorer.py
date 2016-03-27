__author__ = 'Alastair Kerr'

import itertools

from player import Player
from board import Board


class Scorer(object):
    def __init__(self, players=[], board=None):
        """
        Initialise Scorer object with list of Player objects
        :return: None
        """
        for p in players:
            assert isinstance(p, Player)
        assert isinstance(board, Board)
        self.players = players
        self.board = board
        self.scoresMessages = []

    def scoreAll(self):
        """
        Score every player's hand and modify their scores accordingly
        Naive method for now simply adding player's positive scores; TBD implement proper scoring system
        :param players: List of Player objects
        :return: None
        """
        self.scoresMessages = []
        for p in self.players:
            assert isinstance(p, Player)
            p.scoresList = self.scorePlayer(p)
            if (p.scoresList[0] == True):
                self.nullifyPlayerScores(p)

        # Work out all scoring combinations - each player's score is compared against each other player's score
        combinations = itertools.combinations(self.players, 2)
        for combination in combinations:
            scoresMessage = self.evalPlayersScores(combination[0], combination[1])
            self.scoresMessages.append(scoresMessage)


    def scorePlayer(self, player):
        """
        Score the given player's rows, and check if they fouled
        :param player: Player object
        :return: List [Bool fouled, tuple bottom row score, tuple middle row score, tuple top row score]
        """
        assert isinstance(player, Player)

        fouled = False
        placements = self.board.placements[player.playerNumber -1]
        topRowScores = placements.topRow.scoreAndClassify()
        middleRowScores = placements.middleRow.scoreAndClassify()
        bottomRowScores = placements.bottomRow.scoreAndClassify()

        if bottomRowScores[1] >= middleRowScores[1] >= topRowScores[1]:
            pass
        else:
            fouled = True

        return [fouled, bottomRowScores, middleRowScores, topRowScores]

    def nullifyPlayerScores(self, player):
        """
        Take player object and nullifies all row scores (used for dealing with players who fouled)
        :param player: Player object
        :return: None
        """
        assert isinstance(player, Player)
        for i in range(1,4):
            player.scoresList[i][1] = (0, 0)

    def evalPlayersScores(self, player1, player2):
        """
        Takes two player objects and uses scoresList in each to compare rows and adjust player scores appropriately
        :param player1: Player object
        :param player2: Player object
        :return: String describing evaluation (e.g. player 1 won x points off player2, and scooped for +3)
        """
        assert isinstance(player1, Player)
        assert isinstance(player2, Player)

        p1number = player1.playerNumber
        p2number = player2.playerNumber

        if (player1.scoresList[0] == True and player2.scoresList[0] == True):
            return "Player %i and Player %i did not win any points from each other" % (p1number, p2number)

        p1won = self.individualRowWinners(player1, player2)
        p1won += self.compareRoyalties(player1, player2)
        scoopMessage = self.handleScoops(player1, player2)

        if (p1won > 0):
            return "Player %i won %i points from Player %i" % (p1number, p1won, p2number) + scoopMessage
        elif (p1won < 0):
            return "Player %i won %i points from Player %i" % (p2number, - p1won, p1number) + scoopMessage
        else:
            return "Neither Player %i nor Player %i won any points from each other" % (p1number, p2number)

    def individualRowWinners(self, player1, player2):
        """
        Work out winner for each row; take 1 point from loser and give it to winner
        :param player1: Player object
        :param player2: Player object
        :return: int total points player 1 won from player 2
        """
        assert isinstance(player1, Player)
        assert isinstance(player2, Player)

        p1original = player1.score

        # Bottom row
        if (player1.scoresList[1][1] > player2.scoresList[1][1]):
            player1.score += 1
            player2.score -= 1
        elif (player1.scoresList[1][1] < player2.scoresList[1][1]):
            player1.score -=1
            player2.score += 1

        # Middle row
        if (player1.scoresList[2][1] > player2.scoresList[2][1]):
            player1.score += 1
            player2.score -= 1
        elif (player1.scoresList[2][1] < player2.scoresList[2][1]):
            player1.score -= 1
            player2.score += 1

        # Top row
        if (player1.scoresList[3][1] > player2.scoresList[2][1]):
            player1.score += 1
            player2.score -= 1
        elif (player1.scoresList[3][1] < player2.scoresList[3][1]):
            player1.score -= 1
            player2.score += 1

        return player1.score - p1original

    def handleScoops(self, player1, player2):
        """
        Handles scoop logic - adds and subtracts scores as needed, and returns scoop message (if any)
        :param player1: Player object
        :param player2: Player object
        :return: String scoop message
        """
        assert isinstance(player1, Player)
        assert isinstance(player2, Player)

        scoopMessage = ""
        if ( player1.scoresList[1][1] > player2.scoresList[1][1] and \
             player1.scoresList[2][1] > player2.scoresList[2][1] and \
             player1.scoresList[3][1] > player2.scoresList[3][1] ):
            player1.score += 3
            player2.score -= 3
            scoopMessage = " and scooped for +3 points!"

        elif ( player2.scoresList[1][1] > player1.scoresList[1][1] and \
               player2.scoresList[2][1] > player1.scoresList[2][1] and \
               player2.scoresList[3][1] > player1.scoresList[3][1] ):
            player1.score -= 3
            player2.score += 3
            scoopMessage = " and scooped for +3 points!"

        return scoopMessage

    def compareRoyalties(self, player1, player2):
        """
        Work out royalties for each given player, make the appropriate score changes and return this result
        :param player1: Player object
        :param player2: Player object
        :return: int points player 1 won from player 2 (can be negative)
        """
        assert isinstance(player1, Player)
        assert isinstance(player2, Player)

        player1gains = 0
        player1gains += self.calculateRoyalties(player1.scoresList[1][1], 'Bottom')
        player1gains += self.calculateRoyalties(player1.scoresList[2][1], 'Middle')
        player1gains += self.calculateRoyalties(player1.scoresList[3][1], 'Top')
        player1gains -= self.calculateRoyalties(player2.scoresList[1][1], 'Bottom')
        player1gains -= self.calculateRoyalties(player2.scoresList[2][1], 'Middle')
        player1gains -= self.calculateRoyalties(player2.scoresList[3][1], 'Top')

        player1.score += player1gains
        player2.score -= player1gains

        return player1gains

    def calculateRoyalties(self, score, rowName):
        """
        Takes row score tuple and calculates royalties based on row type
        :param score: Score tuple from row eval
        :param rowName: Bottom, Middle or Top
        :return: int points
        """
        assert isinstance(score, tuple)
        assert isinstance(rowName, basestring)
        assert rowName in ['Bottom', 'Middle', 'Top']

        if (score[0] == 0):
            return 0

        if (rowName == 'Bottom'):
            royaltyMappings = {5: 2, 6: 4, 7: 6, 8: 10, 9: 15}
            # Special case for royal flush
            if (score[0] == 9 and score[1] == 14):
                return 25
            try:
                royalty = royaltyMappings[score[0]]
                return royalty
            except:
                return 0

        elif (rowName == 'Middle'):
            royaltyMappings = {4: 2, 5: 4, 6: 8, 7: 12, 8: 20, 9: 30}
            # Special case for royal flush
            if (score[0] == 9 and score[1] == 14):
                return 50
            try:
                royalty = royaltyMappings[score[0]]
                return royalty
            except:
                return 0

        elif (rowName == 'Top'):
            # Top row gets specific royalties for pair of 6s or higher
            if (score[0] == 2):
                if (score[1] < 6):
                    return 0
                return -5 + score[1]
            elif (score[1] == 3):
                return 8 + score[1]
            return 0
