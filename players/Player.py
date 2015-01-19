import argparse
import socket
import sys

import pbots_calc
import calc_functions
import Opponent


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
            if packet_values[0] == "NEWGAME":
                global our_name
                global opp1_name
                global opp2_name
                global bb
                
                our_name = packet_values[1]
                opp1_name = packet_values[2]
                opp2_name = packet_values[3]
                initStackSize = packet_values[4]
                bb = int(packet_values[5])
                timeBank = packet_values[6]

                print "Our name: %s"%our_name
                print "Opp1 name: %s"%opp1_name
                print "Opp2 name: %s"%opp2_name
                
                #initialize a dictionary with all the bots playing
                #initialize the bots as objects first
                ourBot = Opponent.Opponent(our_name,initStackSize,bb)
                opp1 = Opponent.Opponent(opp1_name,initStackSize,bb)
                opp2 = Opponent.Opponent(opp2_name,initStackSize,bb)

                global playersDict            
                playersDict = {our_name: ourBot, opp1_name:opp1, opp2_name:opp2}
                
            if packet_values[0] == "NEWHAND":

                global seat
                global holeCard1
                global holeCard2
                
                global our_bets
                global pot_size
                global big_blind
                global small_blind
                
                our_bets = 0
                pot_size = 0
                #handID is the nth hand
                global handID
                handID = int(packet_values[1])
                #our seat
                seat = int(packet_values[2])
                #our hole cards (our hand)
                holeCard1 = packet_values[3]
                holeCard2 = packet_values[4]



                global playerNames 
                #initial stack sizes
                initStackSizes = [int(packet_values[5]),int(packet_values[6]),int(packet_values[7])]
                #player names ordering
                playerNames = [packet_values[8],packet_values[9],packet_values[10]]
                #number of active players in hand (if player eliminated < 3)
                num_active_players = int(packet_values[11])
                #booleans of active players (same ordering as player names, whether or not they are active in hand (eliminated or not in newhand))
                activePlayers = [packet_values[12],packet_values[13],packet_values[14]]
                #our timebank
                timeBank = packet_values[15]
                


                print "\n"
                print "NEWHAND:%d\n"%handID
                print packet_values
                print "Active Players:%d\n" % num_active_players
                print "Our hand: %s %s"%(holeCard1,holeCard2)


                #initialize our bets depending on whether or not we are blinds (depends on number of players playing)
                #taken into account in the for loop below
                our_bets = 0
                count = 0
                for name in playerNames:
                    bot = playersDict[name]
                    if num_active_players < 3:
                        #take into account heads up play (dealer posts sb, etc)
                        #update eliminated
                        eliminated = playersDict[playerNames[-1]]
                        eliminated.updateEliminated()
                        if count == 0:
                            if name == our_name:
                                #dealer/sb (Heads up)
                                our_bets = 1
                            small_blind = name
                            #updating bot stack sizes for each bot at the start of new hand
                            bot.updateStack(int(initStackSizes[count]) - (bb/2))
                        elif count == 1:
                            if name == our_name:
                                #bb (heads up)
                                our_bets = 2
                            big_blind = name
                            #updating bot stack sizes for each bot at the start of new hand
                            bot.updateStack(int(initStackSizes[count]) - bb)
                        elif count == 2:
                            #updating bot stack sizes for each bot at the start of new hand
                            bot.updateStack(int(initStackSizes[count]))

                    else:
                        if count == 1:
                            small_blind = name
                            #updating bot stack sizes for each bot at the start of new hand
                            bot.updateStack(int(initStackSizes[count]) - (bb/2))
                            if name == our_name:
                                our_bets = 1
                        elif count == 2:
                            big_blind = name
                            #updating bot stack sizes for each bot at the start of new hand
                            bot.updateStack(int(initStackSizes[count]) - bb)
                            if name == our_name:
                                our_bets = 2
                        else:
                            #updating bot stack sizes for each bot at the start of new hand
                            bot.updateStack(int(initStackSizes[count]))
                    


                    #updating bot seat for each bot
                    bot.updateSeat(count+1)
                    
                    #initialize new hand in bot
                    bot.newHand(handID,activePlayers[count])

                    count+=1
                    print name + "'s VPIP: %f"%bot.getVPIP()
                    print name + "'s PFR: %f"%bot.getPFR()
                    print name + "'s estimated fold percentage is %f"% bot.foldPercentage()
                    #print stuff
                    #delete this later
                    if bot.isEliminated():
                        print name + " is eliminated"
                #print more
                if num_active_players < 3:
                    print "\n"+small_blind + " posts small blind/and is dealer, stack size (%d)"%playersDict[small_blind].getStack()
                    print big_blind + " posts big blind, stack size (%d)\n"%playersDict[big_blind].getStack()
                else:
                    print "\n"+small_blind+ " posts small blind, stack size (%d)"%playersDict[small_blind].getStack()
                    print big_blind + " posts big blind, stack size (%d)\n"%playersDict[big_blind].getStack()



            if packet_values[0] == "GETACTION":

                #Parse all inputs from the GETACTION packet
                offset = 0

                #pot_size: int representing size of pot
                pot_size = int(packet_values[1])

                #num_board_cards: integer in {0,3,4,5}
                num_board_cards = int(packet_values[2])

                #board: list of cards on board
                board = []

                if num_board_cards > 0:
                    board = packet_values[3: 3+num_board_cards]
                    offset += num_board_cards

                #stack_sizes: list of 3 ints, starting from 1st seat to 3rd seat
                stack_sizes = packet_values[3+offset: 6+offset]

                #numActivePlayers: int number of players playing current hand
                numActivePlayers = int(packet_values[6+offset])

                #if [activePlayers] list exists:
                if type(packet_values[7+offset]) != int:
                    #activePlayers: list of 3 booleans
                    activePlayers = packet_values[7+offset: 10+offset]
                    offset += 3

                #numLastActions: int number of PerformedActions in lastActions
                numLastActions = int(packet_values[7+offset])  

                if numLastActions > 0:
                    #lastActions: list of PerformedActions
                    lastActions = packet_values[8+offset: 8+offset+numLastActions]
                    offset += numLastActions

                #numLegalActions: int number of LegalActions
                numLegalActions = int(packet_values[8+offset])

                if numLegalActions > 0:
                    #legalActions: list of LegalActions e.g. CALL:2, RAISE:4:100, FOLD
                    legalActions = packet_values[9+offset: 9+offset+numLegalActions]                  
                    offset += numLegalActions

                #timeBank: time left in time bank
                timeBank = packet_values[9+offset]

                #initialize dictionary of available actions
                global avail_actions
                avail_actions = {}
                for action in legalActions:
                    action = action.split(':')
                    #if fold or check is an available action, put in dictionary
                    if action[0] == 'FOLD' or action[0] == 'CHECK':
                        avail_actions[action[0]] = None
                    #if call is an available action, put in dictionary as well as amount to call
                    elif action[0] == 'CALL':
                        avail_actions[action[0]] = [int(action[1])]
                    #if bet or raise is an available action, put in dictionary
                    #as well as range of values you can bet with 
                    elif action[0] == 'BET' or action[0] == 'RAISE':
                        avail_actions[action[0]] = range(int(action[1]), int(action[2])+1)          

                #check last actions


                if num_board_cards == 0:
                    print "\n***PREFLOP***(%d) Board:(%s)"%(pot_size,' '.join(board))
                    print "Our hand: %s %s\n"%(holeCard1,holeCard2)
                elif num_board_cards == 3:
                    print "\n***FLOP***(%d) Board:(%s)"%(pot_size,' '.join(board))
                    print "Our hand: %s %s\n"%(holeCard1,holeCard2)
                elif num_board_cards == 4:
                    print "\n***TURN***(%d) Board:(%s)"%(pot_size,' '.join(board))
                    print "Our hand: %s %s\n"%(holeCard1,holeCard2)
                elif num_board_cards == 5:
                    print "\n***RIVER***(%d) Board:(%s)"%(pot_size,' '.join(board))
                    print "Our hand: %s %s\n"%(holeCard1,holeCard2)
                for lastAction in lastActions:
                    lastAction = lastAction.split(':');
                    #action is word
                    action = lastAction[0]
                    #if action is fold or check

                    if action == 'FOLD' or action == 'CHECK':
                        #name of bot who is doing action
                        name = lastAction[1]
                        #current bot who is doing action (from player dictionary)
                        bot = playersDict[name]
                        if action == 'FOLD':
                            #if folded in preflop round
                            if num_board_cards == 0:       
                                #although might have still be raising /calling thus VPIP might be greater now, and not counting this as 
                                #a VPIP fold (until)
                                bot.foldHandPreflop()
                                #updates the bot's VPIP (willingness to call/raise preflop if not bb or sb (unless raise))       
                            #bot folded, so fold
                            if not (name == our_name):
                                print name + " folds."
                            bot.fold()
                        elif action == 'CHECK':
                            if not (name == our_name):
                                print name + " checks."

                    elif action == 'CALL' or action =='BET' or action =='RAISE':
                        bet = int(lastAction[1])
                        name = lastAction[2]
                        bot = playersDict[name]
                        #if small blind called/raised or big blind called/raised larger than original big blind
                        #or dealer called/raised bb
                        #>= or > (since only call/bet/raise) --> check for bb not included?
                        if bet >= big_blind:
                            if num_board_cards == 0:
                                #take into account reraising (don't want to double count this)
                                #if you look in Opponent class reraising has already been taken into account
                                #(look at self.preFlopCalled and the preFlopCall() function)
                                bot.preFlopCallOrRaise()
                     
                        if action == 'RAISE':
                            #preflop raises - count towards pfr
                            if num_board_cards == 0:
                                bot.preFlopRaise()
                            if not (name == our_name):
                                print name + " raised to %d."%bet

                            
                        elif action == 'BET':
                            if not (name == our_name):
                                print name + " bet %d."%bet

                        elif action == 'CALL':
                            if not (name == our_name):
                                print name + " called %d."%bet

                        else:
                            print "\nnonsense happened\n"

                count = 0
                for name in playerNames:
                    bot = playersDict[name]
                    #update stacks of players once it gets to you
                    bot.updateStack(stack_sizes[count])

                    #update the bot's VPIP
                    bot.updateVPIP()
                    #update the bot's PFR
                    bot.updatePFR()
                    count+=1



                                             
                    

            
#PREFLOP
                if num_board_cards == 0:
                    #later add something to predict an opponents range
                    #of cards by how much they bet/playing style
                    #pbots_calc.calc(hands,board,dead,iters)
                    #equities2: Results instance
                    #2-card equity against random hand, only computed once

                    equities2 = calc_functions.equityCalculator(holeCard1, holeCard2, "", 1000, None, None)
                    if playersDict[opp1_name].inHand() == True and playersDict[opp2_name].inHand() == True:
                        betLogic(board,equities2,pot_size,seat,playersDict[opp1_name],playersDict[opp2_name])
                    elif playersDict[opp1_name].inHand() == True:
                        betLogic(board,equities2,pot_size,seat,playersDict[opp1_name])
                    else:
                        betLogic(board,equities2,pot_size,seat,playersDict[opp2_name])  
#FLOP                       
                elif num_board_cards == 3:

                    equities3 = calc_functions.equityCalculator(holeCard1, holeCard2, board, 1000, None, None)
                    if playersDict[opp1_name].inHand() == True and playersDict[opp2_name].inHand() == True:
                        betLogic(board,equities3,pot_size,seat,playersDict[opp1_name],playersDict[opp2_name])
                    elif playersDict[opp1_name].inHand() == True:
                        betLogic(board,equities3,pot_size,seat,playersDict[opp1_name])
                    else:
                        betLogic(board,equities3,pot_size,seat,playersDict[opp2_name]) 

#TURN
                elif num_board_cards == 4:

                    equities4 = calc_functions.equityCalculator(holeCard1, holeCard2, board, 1000, None, None)
                    if playersDict[opp1_name].inHand() == True and playersDict[opp2_name].inHand() == True:
                        betLogic(board,equities4,pot_size,seat,playersDict[opp1_name],playersDict[opp2_name])
                    elif playersDict[opp1_name].inHand() == True:
                        betLogic(board,equities4,pot_size,seat,playersDict[opp1_name])
                    else:
                        betLogic(board,equities4,pot_size,seat,playersDict[opp2_name])   

#RIVER
                elif num_board_cards == 5:

                    equities5 = calc_functions.equityCalculator(holeCard1, holeCard2, board, 1000, None, None)
                    if playersDict[opp1_name].inHand() == True and playersDict[opp2_name].inHand() == True:
                        betLogic(board,equities5,pot_size,seat,playersDict[opp1_name],playersDict[opp2_name])
                    elif playersDict[opp1_name].inHand() == True:
                        betLogic(board,equities5,pot_size,seat,playersDict[opp1_name])
                    else:
                        betLogic(board,equities5,pot_size,seat,playersDict[opp2_name])   

                    
            elif packet_values[0] == "HANDOVER":
                offset = 0
                handOver_lastActions = []

                handover_stack_sizes = [packet_values[1],packet_values[2],packet_values[3]]
                handOverNumCards = int(packet_values[4])
                if handOverNumCards > 0:
                    handOverBoardCards = packet_values[5:5+handOverNumCards]
                    offset += handOverNumCards

                handOverNum_lastActions = int(packet_values[5+offset])
                if handOverNum_lastActions > 0:
                    handOver_lastActions = packet_values[6+offset: 6+offset+handOverNum_lastActions]

                #look for SHOW to see their cards/what their hand was
                #cards were shown
                shown = False
                for action in handOver_lastActions:
                    actions = action.split(":")
                    action = actions[0]
                    if action == "SHOW":
                        name = actions[3]
                        bot = playersDict[name]
                        bot.showdownAdd()
                        bot.updateWTSD()
                        shown = True                           

                        print name + " WTSD percentage is: %f"%bot.getWTSD()

                    elif action == "WIN" or action == "TIE":
                        print actions
                        name = actions[2]
                        bot = playersDict[name]
                        #if cards were shown, then we can update showdownWins/WTSD
                        if shown:
                            bot.showdownWinAdd()
                            bot.updateWMSD()
                            print name + " W$SD percentage is: %f"%bot.getWMSD()

 



            elif packet_values[0] == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")
        # Clean up the socket.
        s.close()

def reply(action, amount, socket):
    if action == 'FOLD' or action == 'CHECK': 
        if action == 'FOLD':
            print our_name + " folds."
        else:
            print our_name + " checks."

        socket.send(action + "\n")

    elif action == 'CALL' or action == 'BET' or action == 'RAISE':
        if action =='CALL':
            print our_name + " calls %d."%amount
        elif action == 'BET':
            print our_name + " bets %d."%amount
        else:
            print our_name + " raise %d."%amount

        socket.send(action+":"+str(amount)+"\n")


    
def betLogic(board,equities,pot_size,seat,bot1,bot2 = None):
    their_bet = 0
    num_board_cards = len(board)
    num_opp_players = 1
    if "CALL" in avail_actions:
        their_bet = avail_actions["CALL"][0]
    ev = calc_functions.expectedValue(equities,pot_size,their_bet)
    #will want to change this later, not sure when we should start using stats
    if handID >= 10:     
        if "BET" in avail_actions or "RAISE" in avail_actions:
            if bot2 is not None:
                foldEquities = calc_functions.foldEquity(pot_size,ev,bot1.foldPercentage(),bot2.foldPercentage())
                #print "FoldEquities: %f , %f"%(foldEquities[0],foldEquities[1])
            else:
                foldEquities = calc_functions.foldEquity(pot_size,ev,bot1.foldPercentage())
                #print "FoldEquities: %f "%foldEquities[0]

    if bot2 is not None:
        num_opp_players = 2
    else:
        pass
    print our_name +"'s EV: %f"%ev
    print our_name +"'s Equity: %s"%equities.ev[0]
    #also need to take into account stats
    impliedOdds = calc_functions.impliedOdds(equities,pot_size,their_bet)
    averageBetNeeded = impliedOdds / num_opp_players
    print our_name +"'s EV: %f"%ev
    print our_name +"'s Equity: %s"%equities.ev[0]
    print our_name +"'s Implied Odds: %d"%impliedOdds
    if ev >= 0:
        if ev == 0:
            if "CHECK" in avail_actions:
                reply("CHECK", "CHECK", s)
            elif "CALL" in avail_actions:
                minBet = avail_actions["CALL"][0]
                reply("CALL",minBet,s)

        else:
            if "BET" in avail_actions:
                minBet = avail_actions["BET"][0]
                maxBet = avail_actions["BET"][-1]
                reply("BET", minBet,s)
            elif "RAISE" in avail_actions:
                minBet = avail_actions["RAISE"][0]
                maxBet = avail_actions["RAISE"][-1]

                if ev > 10:
                    reply("RAISE", maxBet,s)
                else:
                    reply("RAISE",minBet,s)
            elif "CALL" in avail_actions:
                minBet = avail_actions["CALL"][0]
                reply("CALL",minBet,s)
    else:
        if "CHECK" in avail_actions:
            reply("CHECK", "CHECK", s)
        else:
            reply("FOLD","FOLD",s)

                           

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

