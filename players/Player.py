import argparse
import socket
import sys
import random
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
                            bot.updateAction("",1)
                        elif count == 1:
                            if name == our_name:
                                #bb (heads up)
                                our_bets = 2
                            big_blind = name
                            #updating bot stack sizes for each bot at the start of new hand
                            bot.updateStack(int(initStackSizes[count]) - bb)
                            bot.updateAction("",2)
                        elif count == 2:
                            #updating bot stack sizes for each bot at the start of new hand
                            bot.updateStack(int(initStackSizes[count]))
                            bot.updateAction("",0)

                    else:
                        if count == 1:
                            small_blind = name
                            #updating bot stack sizes for each bot at the start of new hand
                            bot.updateStack(int(initStackSizes[count]) - (bb/2))

                            bot.updateAction("",1)
                            if name == our_name:
                                our_bets = 1
                        elif count == 2:
                            big_blind = name
                            #updating bot stack sizes for each bot at the start of new hand
                            bot.updateStack(int(initStackSizes[count]) - bb)

                            bot.updateAction("",2)
                            if name == our_name:
                                our_bets = 2
                        else:
                            #updating bot stack sizes for each bot at the start of new hand
                            bot.updateStack(int(initStackSizes[count]))
                            bot.updateAction("",0)
                        


                    #updating bot seat for each bot
                    bot.updateSeat(count+1)
                    
                    #initialize new hand in bot
                    #add hand ID?
                    bot.newHand(activePlayers[count])

                    #find the bot's player type at the beginning of the hand
                    bot.findPlayerType()
                    count+=1
                    print name + "'s VPIP: %f"%bot.getVPIP()
                    print name + "'s PFR: %f"%bot.getPFR()
                    print name + "'s estimated fold percentage is %f"% bot.foldPercentage()
                    print name + "'s AF flop/postflop: %f"%bot.getAFflop()
                    print name + "'s Player Type: %s"%bot.read()
                    print name + "'s Seat:%s"%bot.getSeat()
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
                global num_board_cards
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
                            elif num_board_cards >= 3:
                                #folds on the flop
                                bot.updateTotalFoldsFlop()
                                bot.updateAFqFlop()
                            #bot folded, so fold
                            if not (name == our_name):
                                print name + " folds."
                            bot.fold()
                            bot.updateAction("FOLD",0)
                            #bot.updateAFq()
                        elif action == 'CHECK':
                            if not (name == our_name):
                                print name + " checks."
                            bot.updateAction("CHECK")

                    elif action == 'CALL' or action =='BET' or action =='RAISE':
                        bet = int(lastAction[1])
                        name = lastAction[2]
                        bot = playersDict[name]
                        #if small blind called/raised or big blind called/raised larger than original big blind
                        #or dealer called/raised bb
                        #>= or > (since only call/bet/raise) --> check for bb not included?
                        if bet >= bb:
                            if num_board_cards == 0:
                                #take into account reraising (don't want to double count this)
                                #if you look in Opponent class reraising has already been taken into account
                                #(look at self.preFlopCalled and the preFlopCall() function)
                                bot.preFlopCallOrRaise()
                     
                        if action == 'RAISE':
                            #counts towards af 
                            #bot.addBetRaise()
                            #bot.updateAF()
                            #preflop raises - count towards pfr
                            if num_board_cards == 0:
                                bot.preFlopRaise()
                            elif num_board_cards >= 3:
                                bot.addBetRaiseFlop()
                                bot.updateAFflop()
                                bot.updateAFqFlop()
                            if not (name == our_name):
                                print name + " raised to %d."%bet
                            if name == our_name:
                                pass
                            else:
                                bot.updateAction("RAISE",bet,num_board_cards)

                            
                        elif action == 'BET':
                            #counts towards af
                            #bot.addBetRaise()
                            #bot.updateAF()
                            #bot.updateAFq()
                            if num_board_cards >= 3:
                                bot.addBetRaiseFlop()
                                bot.updateAFflop()
                                bot.updateAFqFlop()
                            if not (name == our_name):
                                print name + " bet %d."%bet
                            if name == our_name:
                                pass
                            else:
                                bot.updateAction("BET",bet,num_board_cards)

                        elif action == 'CALL':
                            #counts towards inverse af
                            #bot.addCall()
                            #bot.updateAF()
                            #bot.updateAFq()
                            if num_board_cards >= 3:
                                bot.addCallFlop()
                                bot.updateAFflop()
                                bot.updateAFqFlop()
                            if not (name == our_name):
                                print name + " called %d."%bet
                            #take into account updating our round is screwed up as last actions takes into account our own last action
                            if name == our_name:
                                pass
                            else:
                                bot.updateAction("CALL",bet,num_board_cards)

                        else:
                            print "\nnonsense happened\n"

                count = 0
                for name in playerNames:
                    bot = playersDict[name]
                    #update stacks of players once it gets to you
                    bot.updateStack(stack_sizes[count])
                    bot.updateMRatio()
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
                num_board_cards = int(packet_values[4])
                if num_board_cards > 0:
                    handOverBoardCards = packet_values[5:5+num_board_cards]
                    offset += num_board_cards

                handOverNum_lastActions = int(packet_values[5+offset])
                if handOverNum_lastActions > 0:
                    handOver_lastActions = packet_values[6+offset: 6+offset+handOverNum_lastActions]

                #look for SHOW to see their cards/what their hand was
                #cards were shown
                shown = False
                for lastAction in handOver_lastActions:
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
                            elif num_board_cards >= 3:
                                #folds on the flop
                                bot.updateTotalFoldsFlop()
                                bot.updateAFqFlop()
                            #bot folded, so fold
                            if not (name == our_name):
                                print name + " folds."
                            bot.fold()
                            #bot.updateAFq()
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
                        if bet >= bb:
                            if num_board_cards == 0:
                                #take into account reraising (don't want to double count this)
                                #if you look in Opponent class reraising has already been taken into account
                                #(look at self.preFlopCalled and the preFlopCall() function)
                                bot.preFlopCallOrRaise()
                     
                        if action == 'RAISE':
                            #counts towards af 
                            #bot.addBetRaise()
                            #bot.updateAF()
                            #preflop raises - count towards pfr
                            if num_board_cards == 0:
                                bot.preFlopRaise()
                            elif num_board_cards >= 3:
                                bot.addBetRaiseFlop()
                                bot.updateAFflop()
                                bot.updateAFqFlop()
                            if not (name == our_name):
                                print name + " raised to %d."%bet

                            
                        elif action == 'BET':
                            #counts towards af
                            #bot.addBetRaise()
                            #bot.updateAF()
                            #bot.updateAFq()
                            if num_board_cards >= 3:
                                bot.addBetRaiseFlop()
                                bot.updateAFflop()
                                bot.updateAFqFlop()
                            if not (name == our_name):
                                print name + " bet %d."%bet

                        elif action == 'CALL':
                            #counts towards inverse af
                            #bot.addCall()
                            #bot.updateAF()
                            #bot.updateAFq()
                            if num_board_cards >= 3:
                                bot.addCallFlop()
                                bot.updateAFflop()
                                bot.updateAFqFlop()
                            if not (name == our_name):
                                print name + " called %d."%bet

                        else:
                            print "\nnonsense happened\n"
                

                    elif action == "SHOW":
                        name = lastAction[3]
                        bot = playersDict[name]
                        bot.showdownAdd()
                        bot.updateWTSD()
                        shown = True                           

                        print name + " WTSD percentage is: %f"%bot.getWTSD()

                    elif action == "WIN" or action == "TIE":
                        name = lastAction[2]
                        bot = playersDict[name]
                        #if cards were shown, then we can update showdownWins/WTSD
                        if shown:
                            bot.showdownWinAdd()
                            bot.updateWMSD()
                            print name + " W$SD percentage is: %f"%bot.getWMSD()
                count = 0
                for name in playerNames:
                    bot = playersDict[name]
                    #update stacks of players once it gets to you
                    bot.updateStack(handover_stack_sizes[count])
                    #update m ratio
                    bot.updateMRatio()
                    #update the bot's VPIP
                    bot.updateVPIP()
                    #update the bot's PFR
                    bot.updatePFR()
                    count+=1

            elif packet_values[0] == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                s.send("FINISH\n")
        # Clean up the socket.
        s.close()

def reply(action, amount, socket):
    our_bot = playersDict[our_name]

    if action == 'FOLD' or action == 'CHECK': 
        if action == 'FOLD':
            print our_name + " folds."
        else:
            print our_name + " checks."
        
        our_bot.updateAction(action,0,num_board_cards)
        socket.send(action + "\n")

    elif action == 'CALL' or action == 'BET' or action == 'RAISE':
        if action =='CALL':
            print our_name + " calls %d."%amount
        elif action == 'BET':
            print our_name + " bets %d."%amount
        else:
            print our_name + " raise %d."%amount
        our_bot.updateAction(action,str(amount),num_board_cards)
        socket.send(action+":"+str(amount)+"\n")


    
def betLogic(board,equities,pot_size,our_seat,bot1,bot2 = None):
    their_bet = 0
    #num_board_cards = len(board)
    num_opp_players = 1
    our_equity = equities.ev[0]
    call = False
    bluff = False
    useStats = False
    our_bot = playersDict[our_name]
    our_stack = our_bot.getStack()
    no_reraise = False
    #both dealer/small_blind and 2 players (seat 1), we go first preflop and last post flop
    #if small blind and 3 players, we go 2nd preflop and first postflop
    #if big_blind, we always go last preflop and first post flop if 2 players
    #if big_blind, we always go last preflop, and 2nd post flop if 3 players
    #if dealer and any amount of players, we go first preflop and last postflop

    #dealer is best position post flop
    #big blind is good preflop but screwed postflop if 2 player(have to keep being aggressive if bluffing preflop)
    #semi screwed in 3 player, small blind has to go first there (so they're screwed)
     
    if "CALL" in avail_actions:
        their_bet = avail_actions["CALL"][0]
        no_reraise = True
    if our_bot.getLastRound() is not None:
        our_last_round = our_bot.getLastRound() 
    else:
        our_last_round = 0
    our_last_bet = our_bot.getLastBet()
    print "our last bet of %d was in round %d"%(our_last_bet,our_last_round)
    if (their_bet - our_last_bet >= 0):
        if our_last_round == num_board_cards:
            their_bet = their_bet - our_last_bet
        else:
            pass
    ev = calc_functions.expectedValue(equities,pot_size,their_bet)

    pot_odds = calc_functions.potOdds(pot_size,their_bet)

    if handID > 10:
        useStats = True

    if our_equity >= pot_odds:
        call = True

    #will want to change this later, not sure when we should start using stats
    minFoldPerc = 0.0
    bot2_read = None
    bot2_action = None
    firstAction = False
    if bot2 is not None:
        #finds player reads
        bot1_type = bot1.read()
        bot2_type = bot2.read()
        bot1_action = bot1.getAction()
        bot2_action = bot2.getAction()
        num_opp_players = 2
        #finds the minimum fold percentage of the bots on the table
        #average in the future possibly?
        minFoldPerc = min(bot1.foldPercentage(),bot2.foldPercentage())
        #need bet amount (how much we bet to get them to fold)
        foldEquities = calc_functions.foldEquity(pot_size,ev,bot1.foldPercentage(),bot2.foldPercentage())
        #print "FoldEquities: %f , %f"%(foldEquities[0],foldEquities[1])
        if (bot1_action == "" and bot2_action == ""):
            firstAction = True
    else:
        bot1_type = bot1.read()
        bot1_action = bot1.getAction()
        minFoldPerc = bot1.foldPercentage()
        foldEquities = calc_functions.foldEquity(pot_size,ev,bot1.foldPercentage())
        #print "FoldEquities: %f "%foldEquities[0]
        if bot1_action == "":
            firstAction = True
  
    #do we need this?
    #averageBetNeeded = impliedOdds / num_opp_players
    #also need to take into account stats/player types with impliedOdds
    impliedOdds = calc_functions.impliedOdds(equities,pot_size,their_bet)

    #maxBetEv is the maxBet we should do for our EV to break even, $0
    maxBetEV = calc_functions.maxBetEV(pot_size,our_equity,our_bot.getStack())

    #foldPercentageNeeded = calc_functions.foldPercentageNeeded(pot_size,bet,equity):
    #maxBetFold is the maxBet for our fold EV to be positive,upperbound to our bluff
    #when their fold percentage is 100%, undefined, if 0%, then nothing we bet will make them fold 
    maxBetFold = calc_functions.foldBet(minFoldPerc,pot_size,our_bot.getStack())

    #if nit, we can get them to fold preflop
    #post flop respect their bets
    #maniacs/calling station exploit them for money when we have good hands 
    #cashcows we can exploit them in flop if we know they don't have the nuts / get them to fold, they like to raise preflop
    #if calling station, and they raise, don't call unless you have something good
    #bot1_read/bot1_action

    our_seat = our_bot.getSeat()

    #what can we expect from certain player types?
    #at certain stages of the game using stats we have on them
    #look at our own cards, and chances of winning with what's on the board
    #cashcows are pussies on the flop unless they have something,but aggressive preflop
    #nits - if they're raising/betting preflop to large bets they might have something valuable
    #you can also get nits to fold preflop by bluffing, take into account what they've done (if they limp in, bluff)
    #calling stations - they probably have something good if they raise/bet - make sure you can beat them
    #if our ev < pot_odds, call bool is False (only option is to fold or bluff (+EV from fold equity))



    


    #exploit cashcow by making them fold on the flop
    #if calling stations didn't raise preflop, they normally don't have anything great (unless they're out of character and
    #trying to fool you) but they are willing to go to the river so you can get money from them if you have a good hand


    watch_out = False
    blood_in_the_water = False
    nits_raising = False
    cow_raised = False
    milk_the_cow = False
    round_start = False
    if bot1_type == "CALLING STATION" or bot1_type == "SHARK" or bot1_type == "NIT" and useStats:
        if bot1_action == "RAISE" or bot1_action == "BET":
            watch_out = True

    if bot1_type == "SHARK" and useStats:
        blood_in_the_water = True
    if bot1_type == "CASHCOW" and useStats:
        milk_the_cow = True
        if (bot1_action =="RAISE" or bot1_action == "BET") and useStats:
            cow_raised = True
    if bot1_action == "CALL" and our_bot.getAction() == "CALL":
        round_start = True
    if (bot1_type == "NIT" and (bot1_action == "RAISE" or bot1_action == "BET")) and useStats:
        nits_raising = True

    if bot2 is not None:

        if bot2_type == "SHARK" and useStats:
            blood_in_the_water = True
        if bot2_type == "CASHCOW" and useStats:
            #if bot1 is also a cow
            if milk_the_cow:
                milk_the_cow = True
            else:
                milk_the_cow = False
            if bot2_action =="RAISE" or bot2_action == "BET":
                cow_raised = True

        if (bot2_type == "CALLING STATION" or bot2_type == "SHARK" or bot2_type == "NIT") and useStats:
            if bot2_action == "RAISE" or bot2_action == "BET":
                watch_out = True 
        if (bot2_type =="NIT" and (bot2_action == "RAISE" or bot2_action == "BET")) and useStats:
            nits_raising = True
        if bot2_action == "CALL":
            pass
        else:
            round_start = False
        


    bot1_seat = bot1.getSeat()

    
    bluffMin = float(num_opp_players) * bb + 3.0 * bb
    if bluffMin >= maxBetFold:
        bluffMin = maxBetFold


    if impliedOdds <= 0 and our_equity <= 0.6:
        #don't reraise if this is already a profitable bet
        no_reraise = True
    else:
        if num_board_cards ==0 and our_equity < 0.75:
            no_reraise = True
        #you want to bet a bit more
        else:
            no_reraise = False

    print our_name +"'s EV: %f"%ev
    print our_name +"'s Equity: %s"%equities.ev[0]
    print our_name +"'s Implied Odds: %d"%impliedOdds
    print our_name +"'s maxBetFold: %d"%maxBetFold
    print our_name +"'s maxBetEV: %d\n"%maxBetEV
    our_m = our_bot.getMRatio()

    if our_equity > 0.53 and our_m <= 7:
        action = "BET"
        maxBet = our_stack
        minBet = our_stack
        bettingActions(action,minBet,maxBet)
    elif our_m <=7:
        action ="FOLD"
        bettingActions(action)

    if our_m <= 3:
        action = "BET"
        maxBet = our_stack
        minBet = our_stack
        bettingActions(action,minBet,maxBet)


    if num_board_cards == 0:
        #we're the first action in the round or small blind

        if firstAction or our_name == small_blind:
            #we use equity to fold junk hands
            #junk hands are defined as equity less than 0.43 (arbitrarily)
            #check player type
            if our_equity < 0.46:
                #consider bluffing if nits
                if nits_raising and useStats:
                    #we don't want to fold if we have something good, but this usually means they have something
                    #this bet is the max amount we can bluff for positive fold equity
                    action = "FOLD"
                    bettingActions(action)
                else:
                    #some percentage of the time we should bluff
                    #bet or raise
                    bluffRand = random.random()
                    if bluffRand < 0.35 and their_bet < maxBetFold:
                        action = "BET" 
                        #max bluffing bet
                        maxBet = min(our_stack,max(bluffMin,maxBetFold))
                        minBet = min(bluffMin,maxBetFold)
                        bettingActions(action,minBet,maxBet)
                    else:
                        action = "FOLD"
                        bettingActions(action)

            else:
                pass
        elif our_equity < 0.46:
            #consider bluffing if nits
            if nits_raising and useStats:
                #we don't want to fold if we have something good, but this usually means they have something
                #this bet is the max amount we can bluff for positive fold equity
                print "NITS RAISING FOLD"
                action = "FOLD"
                bettingActions(action)
            elif useStats:
                bluffRand = random.random()
                if bluffRand < 0.35 and their_bet < maxBetFold:
                    action = "BET" 
                    #max bluffing bet
                    maxBet = min(our_stack,max(bluffMin,maxBetFold))
                    minBet = min(bluffMin,maxBet)
                    bettingActions(action,minBet,maxBet)
                else:
                    print "NOT BLUFFING FOLD"
                    action = "FOLD"
                    bettingActions(action)
        #use ev
        if ev >= 0:
            if ev == 0:
                #if our equity is good we want to bet
                #because our ev == 0 if no one has bet yet
                #0.6 is a random threshold
                #check for nits/tight players
                if our_equity >= 0.6 and not no_reraise:
                    action = "BET"
                    maxBet = min(our_stack,max(maxBetEV,bb))
                    minBet = min(bb,maxBet)
                    print "BETTING LOOSE1"
                    bettingActions(action,minBet,maxBet)
                elif our_equity >= 0.6 and no_reraise:
                    action= "CALL"
                    bettingActions(action)
                else:
                    if watch_out and not call:
                        action = "FOLD"
                        print "WATCH OUT EV FOLD 1"
                        bettingActions(action)
                    else:
                        if our_equity >0.45 and not no_reraise:
                            action = "BET"
                            maxBet = max(maxBetEV,bb)
                            minBet = min(bb,maxBet)
                            print "BETTING LESS LOOSE1"
                            bettingActions(action,minBet,maxBet)
                        else:
                            action = "CALL"
                            bettingActions(action)
            elif ev > 0:
                #if our equity is good we want to bet
                #because our ev == 0 if no one has bet yet
                #0.6 is a random threshold
                if our_equity >= 0.6 and not no_reraise:
                    action = "BET"
                    maxBet = min(our_stack,max(maxBetEV,bb))
                    minBet = min(bb,maxBet)
                    print "BETTING LOOSE2"
                    bettingActions(action,minBet,maxBet)
                elif our_equity >= 0.6 and no_reraise:
                    action = "CALL"
                    bettingActions(action)
                else:
                    if watch_out and not call:
                        print "WATCH OUT EV FOLD2"
                        action = "FOLD"
                        bettingActions(action)
                    else:
                        bluffRand = random.random()
                        if bluffRand < 0.3:
                            action = "BET" 
                            #max bluffing bet
                            maxBet = min(our_stack,max(bluffMin,maxBetFold))
                            minBet = min(bluffMin,maxBetFold)
                            bettingActions(action,minBet,maxBet)
                        elif our_equity > 0.45 and not no_reraise:
                            action = "BET"
                            maxBet = min(our_stack,max(bb,maxBetEV))
                            minBet = min(bb,maxBet)
                            print "BETTING LESS LOOSE2"
                            bettingActions(action,minBet,maxBet)
                        else:
                            action = "CALL"
                            bettingActions(action)
        else:
            print "EV FOLD"
            action = "FOLD"
            bettingActions(action)

    #watch out for tight players (sharks), cashcows we can exploit by making them fold
    elif num_board_cards >= 3:
        #if no sharks but there are cashcows
        #and our ev is over a certain threshold (we think we can make them fold)
        if not blood_in_the_water and milk_the_cow:
            #check to see their last actions (if raise/bet, watch out)
            bluffRand = random.random()
            if round_start and bluffRand <= 0.4 and not watch_out and our_equity<0.4:
                #some percentage of the time we should bluff when we have nothing
                #bet or raise
                action = "BET" 
                #max bluffing bet
                maxBet = min(our_stack,max(bb,maxBetFold))
                minBet = min(bluffMin,maxBet)
                bettingActions(action,minBet,maxBet)

            elif bluffRand <= 0.4 and not watch_out and our_equity < 0.4 and not cow_raised:
                #some percentage of the time we should bluff
                #bet or raise
                action = "BET" 
                #max bluffing bet
                maxBet = min(our_stack,max(bb,maxBetFold))
                minBet = min(bluffMin,maxBet)
                bettingActions(action,minBet,maxBet)
            else:
                pass
        if ev >= 0:
            if ev == 0:
                #if our equity is good we want to bet
                #because our ev == 0 if no one has bet yet
                #0.6 is a random threshold
                #check for nits/tight players
                if our_equity >= 0.6 and not no_reraise:
                    action = "BET"
                    maxBet = min(our_stack,max(bb,maxBetEV))
                    minBet = min(bb,maxBet)
                    bettingActions(action,minBet,maxBet)
                elif our_equity >= 0.6 and no_reraise:
                    action= "CALL"
                    bettingActions(action)
                else:
                    if watch_out and not call:
                        action = "FOLD"
                        bettingActions(action)
                    else:
                        bluffRand = random.random()
                        if bluffRand < 0.3 and their_bet < maxBetFold:
                            action = "BET" 
                            #max bluffing bet
                            maxBet = min(our_stack,max(bluffMin,maxBetFold))
                            minBet = min(bluffMin,maxBetFold)
                            bettingActions(action,minBet,maxBet)
                        elif our_equity >0.45 and not no_reraise:
                            action = "BET"
                            maxBet = min(our_stack,max(bb,maxBetEV))
                            minBet = min(bb,maxBet)
                            bettingActions(action,minBet,maxBet)
                        else:
                            action = "CALL"
                            bettingActions(action)
            else:
                #if our equity is good we want to bet
                #because our ev == 0 if no one has bet yet
                #0.6 is a random threshold
                if our_equity >= 0.6:
                    action = "BET"
                    maxBet = min(our_stack,max(bb,maxBetEV))
                    minBet = min(bb,maxBet)
                    bettingActions(action,minBet,maxBet)
                elif our_equity >= 0.6 and no_reraise:
                    action= "CALL"
                    bettingActions(action)
                else:
                    if watch_out and not call:
                        action = "FOLD"
                        bettingActions(action)
                    else:

                        bluffRand = random.random()
                        if bluffRand < 0.4 and their_bet < maxBetFold:
                            action = "BET" 
                            #max bluffing bet
                            maxBet = min(our_stack,max(bluffMin,maxBetFold))
                            minBet = min(bluffMin,maxBetFold)
                            bettingActions(action,minBet,maxBet)
                        elif our_equity >0.5 and not no_reraise:
                            action = "BET"
                            maxBet = min(our_stack,max(bb,maxBetEV))
                            minBet = min(bb,maxBet)
                            bettingActions(action,minBet,maxBet)
                        else:
                            action = "CALL"
                            bettingActions(action)
        else:
            action = "FOLD"
            bettingActions(action)



def bettingActions(action,our_min_bet=None,our_max_bet=None):  
    if our_min_bet == None:
        our_min_bet =0
    if our_max_bet == None:
        our_max_bet  = 1000
    our_bot = playersDict[our_name]
    our_stack = our_bot.getStack()
    if "CALL" in avail_actions:
        minCall = avail_actions["CALL"][0]
    else:
        minCall = 0

    if action == "CALL":
        if "CHECK" in avail_actions:
            reply("CHECK", "CHECK", s)
        elif "CALL" in avail_actions:
            minBet = avail_actions["CALL"][0]
            reply("CALL",minBet,s)

    elif action == "BET":
        if "BET" in avail_actions:
            minBet = avail_actions["BET"][0]
            maxBet = avail_actions["BET"][-1]
            final_max = min(our_max_bet,maxBet)
            if our_min_bet > maxBet:
                final_min = maxBet
            else:
                final_min = max(our_min_bet,minBet)
            final_max = max(final_min,final_max)
            print "final max bet:%d"%final_max
            print "final min bet:%d"%final_min
            print "Bet range: %d %d"%(minBet,maxBet)
            if (final_max - final_min)<= 1.0 :
                bet = final_max
            else:
                bet = random.randint(final_min,final_max)
            if our_max_bet >= our_stack and (our_stack - minCall) < minBet:
                bettingActions("CALL")
            elif our_max_bet < minBet and minBet >10:
                bettingActions("FOLD")

            elif our_max_bet < minBet:
                bettingActions("CALL")
            else:
                reply("BET", bet,s)
        elif "RAISE" in avail_actions:
            minBet = avail_actions["RAISE"][0]
            maxBet = avail_actions["RAISE"][-1]
            final_max = min(our_max_bet,maxBet)
            if our_min_bet > maxBet:
                final_min = maxBet
            else:
                final_min = max(our_min_bet,minBet)
            final_max = max(final_min,final_max)
            print "final max raise:%d"%final_max
            print "final min raise:%d"%final_min
            print "Raise range: %d %d"%(minBet,maxBet)
            if (final_max - final_min) <= 1.0 :
                bet = final_max
            else:
                bet = random.randint(final_min,final_max)
            #don't want it to fold to low minbets
            if our_max_bet >= our_stack and (our_stack - minCall) <= minBet:
                bettingActions("CALL")

            elif our_max_bet < minBet and minBet >10:
                bettingActions("FOLD")

            elif our_max_bet < minBet:
                bettingActions("CALL")
            else:
                reply("RAISE", bet,s)
        elif "CALL" in avail_actions:
            minBet = avail_actions["CALL"][0]
            print "final call min:%d"%minBet
            if our_max_bet >= our_stack and (our_stack - minCall)< minBet:
                reply("CALL",minBet,s)
            elif our_max_bet < minBet and minBet >10:
                bettingActions("FOLD")
            else:
                reply("CALL",minBet,s)
    elif action == "FOLD":
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


