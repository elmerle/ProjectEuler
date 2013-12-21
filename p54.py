CARD, PAIR, TWOPAIR, THREE, STR, FLUSH, FULL, FOUR, SFLUSH, RFLUSH = range(10)

class Card:
    def __init__(self, card):
        if card[0] == 'A':
            self.rank = 14
        elif card[0] == 'T':
            self.rank = 10
        elif card[0] == 'J':
            self.rank = 11
        elif card[0] == 'Q':
            self.rank = 12
        elif card[0] == 'K':
            self.rank = 13
        else:
            self.rank = int(card[0])
        self.suit = card[1]

    def __str__(self):
        return "%s%s" % (self.rank, self.suit)

    def __cmp__(self, other):
        return self.rank - other.rank

def isFlush(cards):
    for i in range(4):
        if cards[i].suit != cards[i+1].suit:
            return False
    return True

def isStraight(ranks):
    return ranks[0] == ranks[1] - 1 and \
           ranks[1] == ranks[2] - 1 and \
           ranks[2] == ranks[3] - 1 and \
           ranks[3] == ranks[4] - 1

def getHand(hand):
    return [Card(hand[i:i+2]) for i in range(0, 15, 3)]

def getN(histogram, n):
    for i in range(12, -1, -1):
        if n == histogram[i]:
            return i + 2

def score(hand):
    cards = sorted(getHand(hand))
    flush = isFlush(cards)
    ranks = [card.rank for card in cards]
    histogram = [0 for i in range(13)]
    for rank in ranks:
        histogram[rank - 2] += 1
    straight = isStraight(ranks)
    if flush and straight:
        if cards[-1].rank == 14:
            return (RFLUSH, 0)
        return (SFLUSH, ranks[-1])
    if flush:
        return (FLUSH, ranks[-1])
    if straight:
        return (STR, ranks[-1])
    if 4 in histogram:
        return (FOUR, getN(histogram, 4))
    if 3 in histogram:
        if 2 in histogram:
            return (FULL, getN(histogram, 3))
        return (THREE, getN(histogram, 3))
    if 2 in histogram:
        rest = list(histogram)
        rest.remove(2)
        if 2 in rest:
            return (TWOPAIR, getN(histogram, 2))
        return (PAIR, getN(histogram, 2))
    return (CARD, ranks[-1])

if __name__ == '__main__':
    count = 0
    file = open('poker.txt', 'r')
    for line in file:
        if score(line[:14]) > score(line[15:]):
            count += 1
        if score(line[:14]) == score(line[15:]):
            print line
    print count