import argparse
import socket
import sys

"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.
"""
class Player:
    def run(self, input_socket):
        # Get a file-object for reading packets from the socket.
        # Using this ensures that you get exactly one packet per read.
        f_in = input_socket.makefile()
        while True:
            # Block until the engine sends us a packet.
            data = f_in.readline().strip()
            # If data is None, connection has closed.
            if not data:
                print "Gameover, engine disconnected."
                break

            # Here is where you should implement code to parse the packets from
            # the engine and act on it. We are just printing it instead.

            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious responses.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, terminate each response with a newline
            # character (\n) or your bot will hang!
            packet_values = data.split()
            
    #BEGIN VARIABLE DEFINITIONS
            if packet_values[0] == "NEWHAND":
                global holeCard1
                global holeCard2

                holeCard1 = Card(packet_values[3][0], packet_values[3][1])
                holeCard2 = Card(packet_values[4][0], packet_values[4][1])
                

            if packet_values[0] == "GETACTION":
                #Obtain all the values from the strings input
                offset = 0 #handle offset/optional values

                #pot_size:= total number of chips in pot
                pot_size = int(packet_values[1])
                #num_board_cards:= number of shown cards (0,3,4,5)
                num_board_cards = int(packet_values[2])
                board = []
                boardCards = []
                if num_board_cards > 0:
                    board = packet_values[3: 3+num_board_cards]
                    
                    boardCards = []
                    for card in board:
                        boardCards.append(Card(card[0], card[1]))
                #boardCards: list of Cards currently on board
                        
                    offset += num_board_cards

                #stack_sizes: list of 3 ints, 1st seat to 3rd seat
                stack_sizes = packet_values[3+offset: 6+offset]

                #numActivePlayers: number of True players (0,1,2,3)
                numActivePlayers = int(packet_values[6+offset])
                
                #if [activePlayers] list exists:
                if type(packet_values[7+offset]) != int:
                    #activePlayers: list of 3 booleans
                    activePlayers = packet_values[7+offset: 10+offset]
                    offset += 3

                #numLastActions: int - # PerformedActions
                numLastActions = int(packet_values[7+offset])
                
                if numLastActions > 0:
                    #lastActions: list of PerformedActions
                    lastActions = packet_values[8+offset: 8+offset+numLastActions]
                    offset += numLastActions
                #numLegalActions: int - # LegalActions
                numLegalActions = int(packet_values[8+offset])

                
                if numLegalActions > 0:
                    #legalActions: list of LegalActions

                    legalActions = packet_values[9+offset: 9+offset+numLegalActions]                  
                    offset += numLegalActions

                #timeBank: amt. of time left
                timeBank = packet_values[9+offset]

                cards = [holeCard1, holeCard2]
    #END VARIABLE DEFINITIONS

                avail_actions = {}
                for action in legalActions:
                    action = action.split(':')
                    if action[0] == 'FOLD' or action[0] == 'CHECK':
                        avail_actions[action[0]] = None

                    elif action[0] == 'CALL':
                        avail_actions[action[0]] = [int(action[1])]
                    elif action[0] == 'BET' or action[0] == 'RAISE':
                        avail_actions[action[0]] = range(int(action[1]), int(action[2])+1)
                #print avail_actions

#Good idea to vary betting strategies to become less predictable

    #PREFLOP
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

    #FLOP
                if len(boardCards) == 3:
                    cards.extend(boardCards)
                    o = pokerHand(cards)
                    score = 15*o[1][0] + o[1][1]
                    print score
                
                # Currently CHECK on every move. You'll want to change this.
                    if 'CHECK' in legalActions:
                        reply('CHECK', 'CHECK', s)
                    elif 'CALL' in avail_actions.keys() and score >= 30:
                        reply('CALL', avail_actions['CALL'][0], s)
                    elif 'RAISE' in avail_actions.keys() and score >= 30:
                        reply('RAISE', avail_actions['RAISE'][0], s)
                    else:
                        reply('FOLD', 'FOLD', s)

                        
                if len(boardCards) >= 3:
                    if 'CHECK' in legalActions:
                        reply('CHECK', 'CHECK', s)
                    else:
                        reply('FOLD', 'FOLD', s)

                        
            elif packet_values[0] == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")
        # Clean up the socket.
        s.close()

def reply(action, amount, socket):
    if action == 'FOLD' or action == 'CHECK':
        socket.send(action + "\n")
    elif action == 'CALL' or action == 'BET' or action == 'RAISE':
        socket.send(action+":"+str(amount)+"\n")
        
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





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Pokerbot.', add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost', help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int, help='Port on host to connect to')
    args = parser.parse_args()

    # Create a socket connection to the engine.
    print 'Connecting to %s:%d' % (args.host, args.port)
    try:
        s = socket.create_connection((args.host, args.port))
    except socket.error as e:
        print 'Error connecting! Aborting'
        exit()

    bot = Player()
    bot.run(s)
