from card import Card


def convertStringToCards(rowString):
    """
    Takes in a row string e.g. "AHADKCKD8S" and converts it into a list of Card objects
    :param rowString string <rank><suit> * 3 or 5 cards
    :return: List of Card objects
    """
    assert isinstance(rowString, basestring)
    rowList = []
    for i in xrange(0, len(rowString), 2):
        rowList.append(Card(rowString[i:i+2]))
    return rowList

def convertCardsToString(cards):
    """
    Converts a list of cards into their representation as a string
    :param cards: List of Card objects
    :return: string cards
    """
    assert isinstance(cards, list)
    cardString = ""
    for c in cards:
        assert isinstance(c, Card)
        cardString += c.card
    return cardString


def compileGameState(game):
    """
    Compiles game state information into dictionary ready to be stored in database
    :param game: game object to compile dict from
    :return: dict Game state
    """
    gameState = {}

    # Top level game information
    gameState['playerCount'] = game.playerCount
    gameState['variant'] = game.variant
    gameState['players'] = {}

    # Player information
    for i in range(1, len(game.players)+1):
        pKey = str(i)
        gameState['players'][pKey] = {}
        pGs = gameState['players'][pKey]
        pGs['playerNumber'] = i
        pGs['score'] = game.players[i-1].score
        pGs['cards'] = convertCardsToString(game.players[i-1].cards)

    # Game state information
    gameState['gameState'] = {}
    gS = gameState['gameState']
    gS['roundNumber'] = game.roundNumber
    gS['roundActionNumber'] = game.roundActionNumber
    gS['firstToAct'] = game.firstToAct
    gS['nextToAct'] = game.nextToAct
    gS['actingOrderPointer'] = game.actingOrderPointer
    gS['deck'] = convertCardsToString(game.board.deck.deck)
    gS['deckPointer'] = game.board.deck.currentPosition

    # Game state placements information
    gS['placements'] = {}
    for i in range(1, len(game.players)+1):
        pKey = str(i)
        gS['placements'][pKey] = {}
        pGs = gS['placements'][pKey]
        pGs['playerNumber'] = i
        pGs['topRow'] = game.board.placements[i-1].topRow.humanReadable()
        pGs['middleRow'] = game.board.placements[i-1].middleRow.humanReadable()
        pGs['bottomRow'] = game.board.placements[i-1].bottomRow.humanReadable()

    return gameState
