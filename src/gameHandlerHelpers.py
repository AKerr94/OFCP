__author__ = 'Alastair Kerr'

from card import Card


def convertCardsListToObj(cards):
    """
    Take a list of card strings and return a list of card objects
    :param cards: List of card strings e.g. ["AH", "AS", "KC"]
    :return: List of card objects
    """
    card_objs = []
    for card in cards:
        card_objs.append(Card(card))
    return card_objs

def convertCardsListToStr(cards):
    """
    Takes a list of card objects and returns a list of card strings
    :param cards: List of card objects
    :return: List of card strings
    """
    card_strs = []
    for card in cards:
        card_strs.append(card.card)
    return card_strs

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
        pGs['cards'] = convertCardsListToStr(game.players[i-1].cards)

    # Game state information
    gameState['gameState'] = {}
    gS = gameState['gameState']
    gS['roundNumber'] = game.roundNumber
    gS['roundActionNumber'] = game.roundActionNumber
    gS['firstToAct'] = game.firstToAct
    gS['nextToAct'] = game.nextToAct
    gS['actingOrderPointer'] = game.actingOrderPointer
    gS['deck'] = convertCardsListToStr(game.board.deck.deck)
    gS['deckPointer'] = game.board.deck.currentPosition

    # Game state placements information
    gS['placements'] = {}
    for i in range(1, len(game.players)+1):
        pKey = str(i)
        gS['placements'][pKey] = {}
        pGs = gS['placements'][pKey]
        pGs['playerNumber'] = i
        pGs['topRow'] = convertCardsListToStr(game.board.placements[i-1].topRow.cardPlacements)
        pGs['middleRow'] = convertCardsListToStr(game.board.placements[i-1].middleRow.cardPlacements)
        pGs['bottomRow'] = convertCardsListToStr(game.board.placements[i-1].bottomRow.cardPlacements)

    return gameState
