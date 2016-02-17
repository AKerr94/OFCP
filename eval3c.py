__author__ = 'Alastair Kerr'


def classify_3(score_or_hand):
    """
    Takes score tuple from simple_3card_evaluator output and classifies hand, or if given hand will score automatically
    e.g. 'Three of a Kind Ks', 'Pair of As, 7 kicker'
    :param score_or_hand: Score tuple (output from simple_3card_evaluator) or hand string
    :return: Human readable hand classification
    """

    if (type(score_or_hand) == tuple):
        score = score_or_hand
    else:
        score = score_3(score_or_hand)

    score_to_classification = {4:'Three of a Kind ', 2:'Pair of ', 1:'High Card: '}

    hand_name = score_to_classification[score[0]]
    if score[0] == 4:
        hand_name += rankValToChar(score[1]) + 's '
    elif score[0] == 2:
        hand_name += rankValToChar(score[1]) + 's, ' + rankValToChar(score[2]) + ' kicker.'
    elif score[0] == 1:
        hand_name += rankValToChar(score[1]) + ', kickers: ' + rankValToChar(score[2]) + ', ' + rankValToChar(score[3])
    else:
        print("Error! Invalid tuple?...")
        return None

    return hand_name

def score_3(hand):
    """
    Takes in 3 card poker hand and evaluates for high card, pair or three of a kind
    :param hand: 3 card poker hand as 6 char string: <rank><suit> 3 times
    :return: Poker hand score
    """
    assert isinstance(hand, basestring)
    assert len(hand) == 6

    hist = generate_histogram(hand)
    if hist != None:
        highestFreq = 0
        nextHighestFreq = 0
        highestFreqRank = 0
        nextHighestFreqRank = 0

        # first pass finds the highest frequency rank
        for item in hist:
            temp = item[1];
            if (temp >= highestFreq and item[0] >= highestFreqRank):
                highestFreq = temp
                highestFreqRank = item[0]

        # second pass finds second highest frequency rank
        if highestFreq < 3:
            for item in hist:
                temp = item[1]
                if (temp >= nextHighestFreq and temp <= highestFreq and item[0] != highestFreqRank):
                    nextHighestFreq = temp
                    nextHighestFreqRank = item[0]

        # if high card, we need to locate third kicker
        if highestFreq == 1:
            for item in hist:
                if item[0] not in (highestFreqRank, nextHighestFreqRank) and item[1] > 0:
                    thirdKicker = item[0]
                    break

         # Three of a Kind
        if (highestFreq == 3):
            thisRank = 4
            return (4,highestFreqRank)

        # Pair
        elif (highestFreq == 2):
            thisRank = 2
            return (2,highestFreqRank,nextHighestFreqRank)

        # High Card
        else:
            thisRank = 1
            return (1,highestFreqRank,nextHighestFreqRank, thirdKicker)

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
    for i in xrange (0,5,2):
        try:
            ranks[i] = rank_char_to_int[hand[i]]
        except:
            ranks[i] = hand[i]

        try:
            temp = int(ranks[i])
        except:
            print("Invalid value! ", hand[i], "could not be converted to int.\n")
            return None

        histogram[temp - 2][1] += 1 # increment frequency for appropriate rank

    return histogram

def rankValToChar(rank):
    """
    Safely attempt to convert a rank to its value e.g. 14 -> A
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


if __name__ == "__main__":
    # Testing functionality
    hand = "ASADJC"
    print score_3(hand)
    print classify_3(hand)