import pbots_calc

example = "As2s:ksqs tsjs9s"
card1 = "as"
card2 = "ad"
board1 = "8s8d8c"
board2 = "8s7s8s"
board3 = "8s8d8c8h"
board4 = "8s8d8c8h9c"


def equityCalculator(holeCard1,holeCard2,board,iterations,theirCards = None, dead= None):
    if theirCards == None:
        theirCards = "xx"
    if board == "":
        pass
    else:
        board = ''.join(board)
    print theirCards
    
    if dead == None:
        dead = ""
        r= ""
    word = holeCard1+holeCard2+":"+theirCards
    
    equities = pbots_calc.calc(word,board,dead,iterations)
    return equities

print equityCalculator(card1,card2,"")
print equityCalculator(card1,card2,board1)
print equityCalculator(card1,card2,board2,"tt+")
print equityCalculator(card1,card2,board3)



"""      
class Card:
#Makes it easier to compare cards
    def __init__(self, rank, suit):
        if rank == 'T': self.rank = 10
        elif rank == 'J': self.rank = 11
        elif rank == 'Q': self.rank = 12
        elif rank == 'K': self.rank = 13
        elif rank == 'A': self.rank = 14
        else: self.rank = int(rank)
        self.suit = suit

    def __str__(self):
        return (self.rank, self.suit)
        
        
def twoCardValuation(card1, card2):
#Given two hole cards, assign an integer between 0 and 10
    if card1.rank == card2.rank:
        if card1.rank == 13 or card1.rank == 14:
            return 10
        elif card1.rank == 11 or card1.rank == 12:
            return 9
        elif card1.rank >= 7 and card1.rank <= 10:
            return 7
        else:
            return 6

    elif card1.suit == card2.suit:
        if abs(card1.rank - card2.rank) <= 4:
            return 5
        else:
            return 4
    else:
        if abs(card1.rank - card2.rank) <= 4:
            return 2
        else:
            return 1

            
def pokerHand(cards):
#A fairly rudimentary method that, given a list of 5 Cards, evaluates the poker
#hand

    frequency = []

    d = {2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: []} 
    s = {'c': [], 'd': [], 'h': [], 's': []}
    
    #d: dictionary holding cards sorted by rank
    #s: dictionary holding cards sorted by suit
    for card in cards:
        rank = card.rank
        suit = card.suit
        d[rank].append(suit)
        s[suit].append(rank)

    for rank in range(2, 15):
        frequency.append(len(d[rank]))

    #check for straight flush
    flush = 0
    straight = 0

    cards.sort(key = lambda x: x.rank)
    
    if abs(cards[0].rank - cards[4].rank) == 4 and 2 not in frequency:
        straight = 1
    elif cards[4].rank == 14 and abs(cards[0].rank - cards[3].rank) == 3 and 2 not in frequency:
        straight = 1

        #will assign valuations later
        #may also want to account for "almost flush", "almost straight"
        

    for suit in ['c', 'd', 'h', 's']:
        if len(s[suit]) == 5:
            flush = 1

    if straight == 1 and flush == 1:
        print 'straight flush'
        return 'straight flush', (9, cards[4].rank)
        
            
    #check for 4-of-a-kind
    if 4 in frequency:
        print 'four of a kind'
        return 'four of a kind', (8, 2 + frequency.index(4))

    #check for full house
    if 3 in frequency and 2 in frequency:
        print 'full house'
        return 'full house', (7, frequency.index(3))

    #check for flush
    if flush == 1:
        print 'flush'
        return 'flush', (6, cards[4].rank)

    #check for straight
    if straight == 1:
        print 'straight'
        return 'straight', (5, cards[4].rank)
        
    #check for 3 of a kind
    if 3 in frequency:
        print 'three of a kind'
        return 'three of a kind', (4, 2 + frequency.index(3))

    #check for 2 pair
    if frequency.count(2) >= 2:
        print 'two pair'
        frequency.reverse()
        return 'two pair', (3, 14 - frequency.index(2))

    #check for one pair
    if 2 in frequency:
        print 'one pair'
        return 'one pair', (2, 2 + frequency.index(2))

    else:
        return 'nothing', (1, cards[4].rank)
"""




"""
                        
                if len(boardCards) == 0:
                    print holeCard1.__str__()
                    print holeCard2.__str__()
                    if twoCardValuation(holeCard1, holeCard2) >= 4:
                        if 'CHECK' in avail_actions.keys():
                            reply('CHECK', 'CHECK', s)
                        elif 'CALL' in avail_actions.keys():
                            reply('CALL', avail_actions['CALL'][0], s)
                        elif 'RAISE' in avail_actions.keys() and twoCardValuation(holeCard1, holeCard2) >= 6:
                            reply('RAISE', avail_actions['RAISE'][0], s)
                        else:
                            reply('FOLD', 'FOLD', s)



                    if twoCardValuation(holeCard1, holeCard2) <= 3:
                        if 'CHECK' in avail_actions.keys():
                            reply('CHECK', 'CHECK', s)
                        elif 'CALL' in avail_actions.keys() and avail_actions['CALL'][0] <= 15:
                            reply('CALL', avail_actions['CALL'][0], s)
                        else:
                            reply('FOLD', 'FOLD', s)
    """

