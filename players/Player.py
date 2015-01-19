import argparse
import socket
import sys

import pbots_calc
import calc_functions


"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.
"""


num_hands = 0
ourOpponentP1Folds = 0
ourrOpponentP2Folds = 0


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
                
                our_name = packet_values[1]
                opp1_name = packet_values[2]
                opp2_name = packet_values[3]
                initStackSize = packet_values[4]
                bb = packet_values[5]
                timeBank = packet_values[6]

                print our_name
                print opp1_name
                print opp2_name
        
                ourBot = Opponent(our_name,initStackSize,bb)
                opp1 = Opponent(opp1_name,initStackSize,bb)
                opp2 = Opponent(opp2_name,initStackSize,bb)
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

                handID = int(packet_values[1])
                seat = int(packet_values[2])
                holeCard1 = packet_values[3]
                holeCard2 = packet_values[4]
                if seat == 1:
                    our_bets = 0
                elif seat == 2:
                    our_bets = 1
                elif seat == 3:
                    our_bets = 2

                global playerNames 
                global initStackSizes   
                initStackSizes = [int(packet_values[5]),int(packet_values[6]),int(packet_values[7])]
                playerNames = [packet_values[8],packet_values[9],packet_values[10]]
                num_active_players = int(packet_values[11])
                activePlayers = [packet_values[12],packet_values[13],packet_values[14]]
                timeBank = packet_values[15]
                count = 0
                print "\n"
                print packet_values
                print "Stacks: "
                print initStackSizes
                print "Players: "
                print playerNames
                print "Active Players:%d" % num_active_players
                for name in playerNames:
                    if num_active_players < 3:
                        #take into account heads up play (dealer posts sb, etc)
                        #update eliminated
                        eliminated = playersDict[playerNames[-1]]
                        eliminated.updateEliminated()
                        if count == 0:
                            if name == our_name:
                                #dealer/sb
                                our_bets = 1
                            small_blind = name
                            print name + " is small blind"
                        if count == 1:
                            if name == our_name:
                                #bb
                                our_bets = 2
                            big_blind = name
                            print name + " is big blind"
                    else:
                        if count == 1:
                            small_blind = name
                            print name + " is small blind"
                        elif count == 2:
                            big_blind = name
                            print name + " is big blind"
                    
                    bot = playersDict[name]
                    bot.updateStack(int(initStackSizes[count]))
                    bot.updateSeat(count+1)
                    bot.newHand(handID,activePlayers[count])

                    count+=1
                            
                
                

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
                

                
                for lastAction in lastActions:
                    lastAction = lastAction.split(':');
                    action = lastAction[0]
                    if action == 'FOLD' or action == 'CHECK':
                        name = lastAction[1]
                        bot = playersDict[name]

                        if num_board_cards == 0:
                            bot.updateVPIP()
                            print name + " VPIP: %f"%bot.getVPIP()

                    elif action == 'CALL' or action =='BET' or action =='RAISE':
                        bet = lastAction[1]
                        name = lastAction[2]
                        bot = playersDict[name]
                        if num_board_cards == 0:
                            if action == 'RAISE' or (name != small_blind and name != big_blind):
                                bot.preflopCall()
                            bot.updateVPIP()
                            print name + " VPIP: %f"%bot.getVPIP()

                count = 0
                for name in playerNames:
                    bot = playersDict[name]
                    bot.updateStack(stack_sizes[count])
                    if activePlayers[count] == True:
                        pass
                    else:
                        if num_board_cards == 0:
                            #preflop fold percentage
                            if not bot.inHand():
                                pass
                            else:
                                bot.foldHandPreflop()
                                print "Bot:" + name +" folds preflop..."
                        bot.fold()

                    bot.updateFoldPer()
                    print name + "'s estimated fold percentage is %f"% bot.foldPercentage()

                                             
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
        socket.send(action + "\n")
    elif action == 'CALL' or action == 'BET' or action == 'RAISE':
        socket.send(action+":"+str(amount)+"\n")


    
def betLogic(board,equities,pot_size,seat,bot1,bot2 = None):
    their_bet = 0
    num_board_cards = len(board)
    if "CALL" in avail_actions:
        their_bet = avail_actions["CALL"][0]
    ev = calc_functions.estimatedValue(equities,pot_size,their_bet)
    if "BET" in avail_actions or "RAISE" in avail_actions:
        if bot2 is not None:
            foldEquities = calc_functions.foldEquity(pot_size,ev,bot1.foldPercentage(),bot2.foldPercentage())
            print "FoldEquities: %f , %f"%(foldEquities[0],foldEquities[1])
        else:
            foldEquities = calc_functions.foldEquity(pot_size,ev,bot1.foldPercentage())
            print "FoldEquities: %f "%foldEquities[0]
        

    print "EV: %f"%ev
    
    if ev >= 0:
        if "CHECK" in avail_actions:
            reply("CHECK", "CHECK", s)
        elif "BET" in avail_actions:
            minBet = avail_actions["BET"][0]
            maxBet = avail_actions["BET"][-1]
            reply("BET", minBet,s)
        elif "CALL" in avail_actions:
            minBet = avail_actions["CALL"][0]
            reply("CALL",minBet,s)

        elif "RAISE" in avail_actions:
            minBet = avail_actions["RAISE"][0]
            maxBet = avail_actions["RAISE"][-1]
            reply("RAISE", minBet,s)
    else:
        if "CHECK" in avail_actions:
            reply("CHECK", "CHECK", s)
        else:
            reply("FOLD","FOLD",s)

            

class Opponent:
    def __init__(self,name,stackSize,bb):
        self.name = name
        self.stackSize = stackSize
        #folds preflop
        self.folds = 0.0
        self.bb = bb
        self.handID = 1
        self.seat = 0
        self.playingHand = True
        self.eliminated = False
        self.playerType = ""
        self.VPIP = 0

        #preflop raising
        self.PFR = 0
        #number of times raised preflop
        self.preFlopRaises = 0


        self.WTSD = 0
        self.preFlopCall = 0
        self.foldPer = 0
        self.showdown = 0

        #wmsd is showdown wins percentage
        #showdownWin is # of times win at showdown
        self.WMSD = 0
        self.showdownWin = 0



    #updates stack value of player
    def updateStack(self,stack):
        self.stackSize = stack   
    #retrieves stacksize of player     
    def stack(self):
        return self.stackSize

    #updates whether eliminated or not
    def updateEliminated(self):
        #if eliminated this becomes true
        self.eliminated = True

    #whether the player is eliminated from tournament or not
    def eliminated(self):
        return self.eliminated

    #m ratio of players (this affects play)
    def MRatio(self):
        return self.stackSize / (self.bb + self.bb / 2.0)

    #foldPercentage is % of times fold preflop
    
    #self.playingHand is a bool for whether a player is playing a hand or not
    def foldPercentage(self):
        return self.foldPer
    #foldHandPreflop is number of times fold preflop
    def foldHandPreflop(self):
        self.folds+= 1.0
    #updates fold percentage
    def updateFoldPer(self):
        self.foldPer = (float(self.folds) / self.handID)
    #for any fold (not just preflop like foldHand, playingHand goes to false)
    def fold(self):
        self.playingHand = False


    #updates seat in newhand of player
    def updateSeat(self,seat):
        self.seat = seat
    #returns seat of player

    def seat(self):
        return self.seat

    #returns whether a player is playing in a hand or not (bool value)
    def inHand(self):
        return self.playingHand
    def newHand(self,handID,playingHand):
        self.handID = handID
        #true unless they're out of the game
        self.playingHand = playingHand

    #name of player
    def getName(self):
        return self.name

    #number of times call a bet if not bb or sb (unless raise from blind and call that)
    def preflopCall(self):
        self.preFlopCall += 1

    #besides bb and sb, number of times raise/call preflop (if bb or sb raises they count)
    def updateVPIP(self):
        self.VPIP = float(self.preFlopCall) / self.handID
    def getVPIP(self):
        return self.VPIP

    #WTSD = percentage of hands that went to showdown
    #self.showdown = # of times went to showdown
    def getWTSD(self):
        return self.WTSD
    def updateWTSD(self):
        self.WTSD = float(self.showdown) / self.handID
        #adds to showdown value (one more showdown counted)
    def showdownAdd(self):   
        self.showdown += 1

    #WMSD = percentage of hands won money at showdown (inversely related to WTSD)
    def getWMSD(self):
        return self.WMSD
    def updateWMSD(self):
        self.WMSD = float(self.showdownWin) / self.handID
    #adds to showdown win value (one more showdown counted)
    def showdownWinAdd(self):   
        self.showdownWin += 1

    #PFR = preflop raising
    def getPFR(self):
        return self.PFR
    def updatePFR(self):
        self.PFR = float(self.preFlopRaises) / self.handID

    def preFlopRaiseAdd(self):
        self.preFlopRaises +=1


    #finds player type according to stats
    def findPlayerType():
        VPIP_threshold = 0
        PFR_threshold = 0
        WTSD_threshold = 0
        vpip_range = 0
        if self.VPIP > VPIP_threshold:
            if self.PFR >= PFR_threshold:
                self.playerType = "LAG"

            else:
                self.playerType = "FISH"
        elif self.VPIP > (VPIP_threshold - vpip_range) and self.VPIP < (VPIP_threshold + vpip_range):
            #average VPIP and PFR
            if self.PFR >= PFR_threshold:
                self.playerType = "TAG"
        if self.WTSD >= WTSD_threshold:
            self.playerType = "CALL"
        else:
            self.playerType = "ROCK"
            
        
        
    
        
                                    

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

