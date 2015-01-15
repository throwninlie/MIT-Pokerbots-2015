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
                global equities2


                seat = packet_values[2]
                holeCard1 = packet_values[3]
                holeCard2 = packet_values[4]
                #later add something to predict an opponents range
                #of cards by how much they bet/playing style
                #pbots_calc.calc(hands,board,dead,iters)
                equities2 = calculatorTest.equityCalculator(holecard1,holecard2,"",1000)
                #equities2 := 2-card equities, only computed once
                

            if packet_values[0] == "GETACTION":
                #Obtain all the values from the strings input
                offset = 0 #handle offset/optional values

                #pot_size:= total number of chips in pot
                pot_size = int(packet_values[1])
                #num_board_cards:= number of shown cards (0,3,4,5)
                num_board_cards = int(packet_values[2])
                board = []

                #boardCards = []
                if num_board_cards > 0:
                    board = packet_values[3: 3+num_board_cards]

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


def preflop():
    #PREFLOP
    if len(board) == 0:
        
        print holeCard1, holeCard2, equities2
    
    #random basic preflop strategy, should be changed
    #seems to beat the random bots
        if equity2 > .34:
            if "CHECK" in avail_actions.keys():
                reply("CHECK", "CHECK", s)
            elif "RAISE" in avail_actions.keys():
                reply("RAISE", avail_actions["RAISE"][0], s)
            elif "CALL" in avail_actions.keys():
                reply("CALL", avail_actions["CALL"][0], s)
            else:
                reply("FOLD", "FOLD", s)
        elif equity2 <= .34:
            reply("FOLD", "FOLD", s)
    

def turn():

def river()

def fold():
    #you should never fold if everyone else has checked
def raiseBet():

def bet():

def check():
    
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

