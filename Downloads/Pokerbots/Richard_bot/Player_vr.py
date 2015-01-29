import argparse
import socket
import sys

import pbots_calc
import calculatorTest


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

                global seat
                global holeCard1
                global holeCard2
                global stack_sizes_init


                seat = int(packet_values[2])
                holeCard1 = packet_values[3]
                holeCard2 = packet_values[4]
                stack_sizes_init = packet_values[5:8]
                print stack_sizes_init

                #later add something to predict an opponents range
                #of cards by how much they bet/playing style
                #pbots_calc.calc(hands,board,dead,iters)




                global equities2
                global equities3
                global equities4
                global equities5
                #equities2,3,4,5 represent Results objects corresponding to your
                #and opp's equities, given unknown opp hands. Only computed once
                equities2 = None
                equities3 = None
                equities4 = None
                equities5 = None
                
                

            if packet_values[0] == "GETACTION":
                #Parse all inputs from the GETACTION packet

                #pot_size: int representing size of pot
                #num_board_cards: integer in {0,3,4,5}
                #board: list of cards on board
                #stack_sizes: list of 3 ints, starting from 1st seat to 3rd seat
                #numActivePlayers: int number of players playing current hand
                #activePlayers: list of 3 booleans
                #numLastActions: int number of PerformedActions in lastActions
                #lastActions: list of PerformedActions
                #numLegalActions: int number of LegalActions
                #legalActions: list of LegalActions e.g. CALL:2, RAISE:4:100, FOLD
                #timeBank: time left in time bank
                
                offset = 0
                
                pot_size = int(packet_values[1])
                num_board_cards = int(packet_values[2])
                
                board = []
                if num_board_cards > 0:
                    board = packet_values[3: 3+num_board_cards]
                    offset += num_board_cards

                stack_sizes = packet_values[3+offset: 6+offset]
                print 'stack_sizes', stack_sizes
                print 'seat', seat, '\n'

                our_bets = int(stack_sizes_init[seat-1]) - int(stack_sizes[seat-1])
                
                numActivePlayers = int(packet_values[6+offset])           
                #if [activePlayers] list exists:
                if type(packet_values[7+offset]) != int:
                    activePlayers = packet_values[7+offset: 10+offset]
                    offset += 3


                numLastActions = int(packet_values[7+offset])          
                if numLastActions > 0:
                    lastActions = packet_values[8+offset: 8+offset+numLastActions]
                    offset += numLastActions
                numLegalActions = int(packet_values[8+offset])

                
                if numLegalActions > 0:
                    legalActions = packet_values[9+offset: 9+offset+numLegalActions]                  
                    offset += numLegalActions

                timeBank = packet_values[9+offset]

#avail_actions
                global avail_actions
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
                #print holeCard1, holeCard2, board
                print holeCard1, holeCard2, board, 'eq = ', calculatorTest.equityCalculator(holeCard1, holeCard2, board, 100).ev[0]
                print 'our_bets =', our_bets, 'pot_size =', pot_size


#equity/minBet

#minBet = 10
#lower equity
#minBet = 155
#need higher equity to match
                    


            
#PREFLOP
                if num_board_cards == 0:
                    #later add something to predict an opponents range
                    #of cards by how much they bet/playing style
                    #pbots_calc.calc(hands,board,dead,iters)
                    #equities2: Results instance
                    #2-card equity against random hand, only computed once

                    
                    preflop(equities2, avail_actions, pot_size, our_bets, board)
#FLOP                       
                elif num_board_cards == 3:
                    flop(equities3, avail_actions, pot_size, our_bets, board)
                    
#TURN
                elif num_board_cards == 4:
                    turn(equities4, avail_actions, pot_size, our_bets, board)

#RIVER
                elif num_board_cards == 5:
                    river(equities5, avail_actions, pot_size, our_bets, board)

                    
            elif packet_values[0] == "HANDOVER":
                offset = 0
                stackSizes = packet_values[1:4]
                numBoardCards = int(packet_values[4])

                if numBoardCards > 0:
                    print 'n', numBoardCards
                    boardCards = packet_values[5: 5+numBoardCards]
                    offset += numBoardCards

                numLastActions = int(packet_values[5+offset])
                if numLastActions > 0:
                    lastActions = packet_values[6+offset: 6+offset+numLastActions]
                    offset += numLastActions

                for action in lastActions:
                    action = action.split(":")

                print lastActions
                
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



##def equityCalculator(holeCard1,holeCard2,board,iterations,theirCards = None, dead= None):
##    if theirCards == None:
##        theirCards = "xx"
##    if board == "":
##        pass
##    else:
##        board = ''.join(board)
##    print theirCards
##    
##    if dead == None:
##        dead = ""
##        r= ""
##    word = holeCard1+holeCard2+":"+theirCards
##    
##    equities = pbots_calc.calc(word,board,dead,iterations)
##    return equities

def estimatedValue(equities,pot_size,our_bets,bet):
    ourEquity = equities.ev[0]
    theirEquity = equities.ev[1]

        
    winAmt = pot_size - our_bets - bet
    loseAmt = our_bets + bet
    
    estimated_value = ourEquity * winAmt - (1-ourEquity) * loseAmt
    print 'The EV is ', estimated_value
    return estimated_value

##def impliedOdds(equities,pot_size,bet):
##    ourEquity = equities.ev[0]
##    x = (float) bet / ourEquity
##    y = pot_size + bet + bet
##    impliedOdds = x - y
##    return impliedOdds

##def bet(equities):
##    
##    bet = 0
##    if "CALL" in avail_actions:
##        bet = avail_actions["CALL"][0]
##    ev = estimatedValue(equities,pot_size,our_bets,bet)
##    if ev > 0:
##        
##        
##    if "BET" in avail_actions:
##        minBet = avail_actions["BET"][0]
##        maxBet = avail_actions["BET"][-1]
##    elif "RAISE" in avail_actions:
##        minBet = avail_actions["RAISE"][0]
##        maxBet = avail_actions["RAISE"][-1]
##    
    
#PREFLOP
def preflop(equities2, avail_actions, pot_size, our_bets, board):
    if equities2 == None:
        equities2 = calculatorTest.equityCalculator(holeCard1, holeCard2, board, 1000, None, None)
    #superior
    if holeCard1[0] == holeCard2[0] and holeCard1[0] in ['A', 'K', 'Q', 'J']:
        if 'CALL' in avail_actions.keys():
            print 'We called ', avail_actions["CALL"][0], '\n'
            reply('CALL', avail_actions['CALL'][0], s)
            
        elif 'RAISE' in avail_actions.keys():
            print 'We raised ', avail_actions['RAISE'][0], '\n'
            reply('RAISE', avail_actions['RAISE'][0], s)
            
        elif 'BET' in avail_actions.keys():
            reply('BET', avail_actions['BET'][0], s)
            
        elif 'CHECK' in avail_actions.keys():
            print 'We checked'
            reply('CHECK', 'CHECK', s)

#good
    elif equities2.ev[0] > .5 or holeCard1[0] == holeCard2[0] or holeCard1[1] == holeCard2[1] or 'A' in [holeCard1[0], holeCard2[0]]:
        if 'CHECK' in avail_actions.keys():
            print 'We checked. \n'
            reply("CHECK", "CHECK", s)
        elif 'CALL' in avail_actions.keys():
            callAmt = avail_actions['CALL'][0]
            print 'We called ', callAmt, '\n'
            reply('CALL', callAmt, s)
            
        elif 'RAISE' in avail_actions.keys():
            raiseAmt = avail_actions['RAISE'][0]
            print 'We raised ', raiseAmt, '\n'
            reply('RAISE', raiseAmt, s)


    else:
        if 'CHECK' in avail_actions.keys():
            print 'We checked. \n'
            reply('CHECK', 'CHECK', s)


        else:
            print 'We folded. \n'
            reply('FOLD', 'FOLD', s)
                

            
#just playing around       
                
#FLOP
def flop(equities3, avail_actions, pot_size, our_bets, board):
    if equities3 == None:
        equities3 = calculatorTest.equityCalculator(holeCard1, holeCard2, board, 1000, None, None)
    bet = 0
    if "CALL" in avail_actions.keys():
        bet = avail_actions["CALL"][0]
    elif "RAISE" in avail_actions.keys():
        bet = avail_actions["RAISE"][0]
    elif "BET" in avail_actions.keys():
        bet = avail_actions["BET"][0]
    print 'bet =', bet
        
    EV = estimatedValue(equities3, pot_size, our_bets, bet)

    potEquity = pot_size*equities3.ev[0]
    potOdds = float(pot_size)/bet
    print pot_size, EV, bet
    print 'pE = ', potEquity, 'pO = ', potOdds

    if equities3.ev[0] > 0.8:
        if 'RAISE' in avail_actions.keys():
            reply("RAISE", avail_actions['RAISE'][0], s)

    if potOdds > potEquity:
        if "CHECK" in avail_actions.keys():
            print 'We checked. \n'
            reply("CHECK", "CHECK", s)
        elif "CALL" in avail_actions.keys():
            print 'We called ', bet, '\n'
            reply("CALL", bet, s)
        elif "RAISE" in avail_actions.keys():
            print 'We raised ', bet,'\n'
            reply("RAISE", bet, s)


    elif potOdds <= potEquity:
        if "CHECK" in avail_actions.keys():
            print 'We checked. \n'
            reply("CHECK", "CHECK", s)
        else:
            print 'We folded \n'
            reply("FOLD", "FOLD", s)

#TURN
def turn(equities4, avail_actions, pot_size, our_bets, board):
    if equities4 == None:
        equities4 = calculatorTest.equityCalculator(holeCard1, holeCard2, board, 1000, None, None)
    bet = 0
    if "CALL" in avail_actions.keys():
        bet = avail_actions["CALL"][0]
    elif "RAISE" in avail_actions.keys():
        bet = avail_actions["RAISE"][0]
    elif "BET" in avail_actions.keys():
        bet = avail_actions["BET"][0]

    print 'bet =', bet

        
    EV = estimatedValue(equities4, pot_size, our_bets, bet)

    potEquity = pot_size*equities4.ev[0]
    potOdds = float(pot_size)/bet
    print pot_size, EV, bet
    print 'pE = ', potEquity, 'pO = ', potOdds

    if equities4.ev[0] > 0.9:
        if "RAISE" in avail_actions.keys():
            reply("RAISE", avail_actions["RAISE"][0], s)
        elif "CALL" in avail_actions.keys():
            reply("CALL", avail_actions["CALL"][0], s)


    if potOdds > potEquity:
        if "CHECK" in avail_actions.keys():
            print 'We checked. \n'
            reply("CHECK", "CHECK", s)
        elif "CALL" in avail_actions.keys():
            print 'We called ', bet, '\n'
            reply("CALL", bet, s)
        elif "RAISE" in avail_actions.keys():
            print 'We raised ', bet,'\n'
            reply("RAISE", bet, s)


    elif potOdds <= potEquity:
        if "CHECK" in avail_actions.keys():
            print 'We checked. \n'
            reply("CHECK", "CHECK", s)
        else:
            print 'We folded \n'
            reply("FOLD", "FOLD", s)

#RIVER
def river(equities5, avail_actions, pot_size, our_bets, board):
    if equities5 == None:
        equities5 = calculatorTest.equityCalculator(holeCard1, holeCard2, board, 1000, None, None)
    bet = 0
    if "CALL" in avail_actions.keys():
        bet = avail_actions["CALL"][0]
    elif "RAISE" in avail_actions.keys():
        bet = avail_actions["RAISE"][0]
    elif "BET" in avail_actions.keys():
        bet = avail_actions["BET"][0]
    print 'bet = ', bet
    
    EV = estimatedValue(equities5, pot_size, our_bets, bet)
    
    potEquity = pot_size*equities5.ev[0]
    potOdds = float(pot_size)/bet
    print pot_size, EV, bet
    print 'pE = ', potEquity, 'pO = ', potOdds

    if equities5.ev[0] > 0.85:
        if "RAISE" in avail_actions.keys():
            reply("RAISE", avail_actions["RAISE"][0], s)
        elif "CALL" in avail_actions.keys():
            reply("CALL", avail_actions["CALL"][0], s)

    
    if potOdds > potEquity:
        if "CHECK" in avail_actions.keys():
            print 'We checked. \n'
            reply("CHECK", "CHECK", s)
        elif "CALL" in avail_actions.keys():
            print 'We called ', bet, '\n'
            reply("CALL", bet, s)
        elif "RAISE" in avail_actions.keys():
            print 'We raised ', bet,'\n'
            reply("RAISE", bet, s)


    elif potOdds <= potEquity:
        if "CHECK" in avail_actions.keys():
            print 'We checked. \n'
            reply("CHECK", "CHECK", s)
        else:
            print 'We folded \n'
            reply("FOLD", "FOLD", s)

    

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

    

