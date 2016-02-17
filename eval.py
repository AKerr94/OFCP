__author__ = 'Alastair Kerr'


def classify_5(score_or_hand):
    """
    Takes score tuple from simple_3card_evaluator output and classifies hand, or if given hand will score automatically
    e.g. 'Three of a Kind Ks', 'Pair of As, 7 kicker'
    :param score_or_hand: Score tuple (output from simple_3card_evaluator) or hand string
    :return: Human readable hand classification
    """

    if (type(score_or_hand) == tuple):
        score = score_or_hand
    else:
        score = score_5(score_or_hand)

    score_to_classification = {9: 'Straight Flush ', 8: 'Four of a Kind ', 7: 'Full House ', 6: 'Flush ',\
                               5: 'Straight ', 4:'Three of a Kind ', 3: 'Two Pair ', 2:'Pair of ', 1:'High Card: '}

    hand_name = score_to_classification[score[0]]
    if score[0] == 9:
        hand_name += rankValToChar(score[1]) + ' high'
    elif score[0] == 8:
        hand_name += rankValToChar(score[1]) + 's, ' + rankValToChar(score[2]) + ' kicker'
    elif score[0] == 7:
        hand_name += rankValToChar(score[1]) + 's full of ' + rankValToChar(score[2]) + 's'
    elif score[0] == 6:
        hand_name += rankValToChar(score[1]) + ' high, ' + rankValToChar(score[2]) + ' kicker'
    elif score[0] == 5:
        hand_name += rankValToChar(score[1]) + ' high'
    elif score[0] == 4:
        hand_name += rankValToChar(score[1]) + 's, ' + rankValToChar(score[2]) + ' kicker'
    elif score[0] == 3:
        hand_name += rankValToChar(score[1]) + 's and ' + rankValToChar(score[2]) + 's, ' + rankValToChar(score[3]) + ' kicker'
    elif score[0] == 2:
        hand_name += rankValToChar(score[1]) + 's, ' + rankValToChar(score[2]) + ' kicker'
    elif score[0] == 1:
        hand_name += rankValToChar(score[1]) + ', kickers: ' + rankValToChar(score[2]) + ', ' + rankValToChar(score[3])
    else:
        print("Error! Invalid tuple?...")
        return None

    return hand_name

def score_5(hand):
    """
    Takes in 3 card poker hand and evaluates for high card, pair or three of a kind
    :param hand: 3 card poker hand as 6 char string: <rank><suit> 3 times
    :return: Poker hand score
    """
    assert isinstance(hand, basestring)
    assert len(hand) == 10

    hist = generate_histogram(hand)
    if hist != None:
        highestFreq = 0
        nextHighestFreq = 0
        highestFreqRank = 0
        nextHighestFreqRank = 0

        # first pass finds the highest frequency rank
        for item in hist:
            temp = item[1]
            if (temp >= highestFreq and item[0] >= highestFreqRank):
                highestFreq = temp
                highestFreqRank = item[0]

        # second pass finds second highest frequency rank
        for item in hist:
            temp = item[1]
            if (temp >= nextHighestFreq and temp <= highestFreq and item[0] != highestFreqRank):
                nextHighestFreq = temp
                nextHighestFreqRank = item[0]

        # Third pass
        if (highestFreq <= 3 and nextHighestFreq <= 2):
            for item in hist:
                if item[0] not in (highestFreqRank, nextHighestFreqRank) and item[1] > 0:
                    thirdKicker = item[0]
                    break

        # Four of a Kind
        if (highestFreq == 4):
            return (8, highestFreqRank, nextHighestFreqRank)

        if (highestFreq == 3):
            # Full House
            if (nextHighestFreq == 2):
                return (7, highestFreqRank, nextHighestFreqRank)
            # Three of a Kind
            return (4, highestFreqRank, nextHighestFreqRank, thirdKicker)

        elif (highestFreq == 2):
            # Two Pair
            if (nextHighestFreq == 2):
                return (3, highestFreqRank, nextHighestFreqRank, thirdKicker)
            # Pair
            return (2, highestFreqRank, nextHighestFreqRank, thirdKicker)

        else:
            # Check straights and flushes
            score = checkStraightFlushes(hand)
            if (score):
                return score
            # High Card
            return (1,highestFreqRank, nextHighestFreqRank, thirdKicker)

    else:
        return None

def checkStraightFlushes(hand):
    """
    Return hand rank if a straight or flush, else returns None
    :param hand: 10 char string representing 5 card poker hand
    :return: Hand ranking
    """
    flush = False
    straight = False

    ranks = []
    suits = []
    for i in xrange(0,9,2):
        ranks.append(int(rankValToChar(hand[i])))
    for i in xrange(1,10,2):
        suits.append(hand[i])

    # Check Flush
    firstSuit = suits[0]
    count = 0
    for suit in suits:
        if suit != firstSuit:
            break
        count += 1
    if (count == 5):
        flush = True

    # Check Straight
    ranks.sort()
    if (ranks[4] - ranks[0] == 4):
        straight = True

    # Return
    if (flush and straight):
        return (9, int(rankValToChar(ranks[4])))
    elif (flush):
        return (6, int(rankValToChar(ranks[4])), int(rankValToChar(ranks[3])))
    elif (straight):
        return (5, int(rankValToChar(ranks[4])))
    else:
        return None


def generate_histogram(hand):
    """
    Histogram mapping frequency of each card rank to check for pairs, trips etc.
    hist [card x][0] = card x's rank value, [card x][1] = card x's rank frequency
    :param hand: 3 card poker hand as 6 char string
    :return: Histogram (list of lists with frequency of each card rank in given hand)
    """

    histogram = [
        [2, 0],     # Deuce
        [3, 0],     # 3
        [4, 0],     # 4
        [5, 0],     # 5
        [6, 0],     # 6
        [7, 0],     # 7
        [8, 0],     # 8
        [9, 0],     # 9
        [10, 0],    # 10
        [11, 0],    # Jack
        [12, 0],    # Queen
        [13, 0],    # King
        [14, 0]     # Ace
    ]

    # strip hand name to get rank and then update frequencies in histogram
    ranks = [0,0,0,0,0]
    rank_char_to_int = {'T':'10', 'J':'11', 'Q':'12', 'K':'13', 'A':'14'}
    count = 0
    for i in xrange (0,9,2):
        try:
            ranks[count] = rank_char_to_int[hand[i]]
        except:
            ranks[count] = hand[i]

        try:
            temp = int(ranks[count])
        except:
            print("Invalid value! ", hand[i], "could not be converted to int.\n")
            return None

        histogram[temp - 2][1] += 1 # increment frequency for appropriate rank
        count += 1

    return histogram

def rankValToChar(rank):
    """
    Safely attempt to convert a rank to its char e.g. 14 -> A
    :param rank: String or int 'rank'
    :return: Rank char
    """
    if (type(rank) != int):
        try:
            rank = int(rank)
        except:
            raise AttributeError("Invalid rank parameter in rankValToChar function")
    assert 2 <= rank <= 14

    rank_val_to_char = {'10':'T', '11':'J', '12':'Q', '13':'K', '14':'A'}
    try:
        rank = rank_val_to_char[str(rank)]
    except:
        pass
    return str(rank)

def rankCharToVal(rank):
    """
    Safely attempt to convert a rank to its value e.g. A -> 14
    :param rank: String 'rank'
    :return: Rank int
    """
    rank_char_to_int = {'T':'10', 'J':'11', 'Q':'12', 'K':'13', 'A':'14'}
    try:
        rank = rank_char_to_int[rank]
    except:
        try:
            rank = int(rank)
        except:
            raise AttributeError("Invalid rank parameter in rankCharToVal function")
    return int(rank)


if __name__ == "__main__":
    # Testng functionality
    hand = "3C4C5C6C7C"
    print("%s, %s") % (score_5(hand), classify_5(hand))
