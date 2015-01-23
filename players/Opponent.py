class Opponent:
    def __init__(self,name,stackSize,bb):
        self.name = name
        self.stackSize = int(stackSize)
        self.bb = int(bb)
        #hands played (not counting when eliminated), not just handID
        self.handsPlayed = 0.0
        self.seat = 0.0
        self.playingHand = True
        self.eliminated = False

        #type of player
        self.playerType = "UNKNOWN"

        ##FOLD PERCENTAGE##
        #percent of times folded preflop
        self.foldPer = 0.0
        #folds preflop
        self.foldsPreFlop = 0.0

        #total folds at the flop, num board cards == 3
        self.totalFoldsFlop = 0.0

        ##VPIP##
        #percent of times voluntarily put money in pot
        self.VPIP = 0.0
        self.preFlopCall = 0.0
        #whether he has already contributed to pot preflop in this hand (so as to not double count preflopCall())
        self.preFlopCalled = False

        ##PFR##
        #preflop raising
        self.PFR = 0.0
        #number of times raised preflop
        self.preFlopRaises = 0.0
        #whether he has already raised preflop (so as to not double count)
        self.preFlopRaised = False
    
        ##WTSD##
        #percent of times went to showdown
        self.WTSD = 0.0
        #number of showdowns
        self.showdown = 0.0

        ##WMSD##
        #wmsd is showdown wins percentage
        self.WMSD = 0.0
        #showdownWin is # of times win at showdown
        self.showdownWin = 0.0

        ##AGGRESSION FACTOR FLOP##
        #AFflop is percentage of time (bet + raise)/calls
        self.AFflop = 0.0
        self.totalCallsFlop = 0.0
        self.totalBetRaiseFlop = 0.0

        #FLOP AGGRESION FREQUENCY
        self.AFq = 0.0

        #M ratio
        self.M = 0.0

        #last player's action
        self.action = ""
        self.lastBet = 0.0
    def updateAction(self,action,bet = None):
        self.action = action
        if bet is not None:
            self.lastBet = int(bet)
    def getAction(self):
        return self.action
    def getLastBet(self):
        return self.lastBet

    #updates stack value of player
    def updateStack(self,stack):
        self.stackSize = int(stack)  
    #retrieves stacksize of player     
    def getStack(self):
        return int(self.stackSize)

    #updates whether eliminated or not
    def updateEliminated(self):
        #if eliminated this becomes true
        self.playingHand = False
        self.eliminated = True

    #whether the player is eliminated from tournament or not
    def isEliminated(self):
        return self.eliminated

    #m ratio of players (this affects play)
    def updateMRatio(self):
        self.M = int(self.stackSize) / (int(self.bb) + int(self.bb) / 2.0)
    def getMRatio(self):
        return self.M

    #foldPercentage is % of times fold preflop
    
    #self.playingHand is a bool for whether a player is playing a hand or not
    def foldPercentage(self):
        return self.foldPer
    #foldHandPreflop is number of times fold preflop
    def foldHandPreflop(self):
        self.foldsPreFlop += 1.0
        self.fold()
        self.updateFoldPer()

    #updates fold percentage
    def updateFoldPer(self):
        self.foldPer = (float(self.foldsPreFlop) / self.handsPlayed)
    #for any fold (not just preflop like foldHand, playingHand goes to false)
    def fold(self):
        self.playingHand = False
    #updates total folds flop (for Afq flop)
    def updateTotalFoldsFlop(self):     
        self.totalFoldsFlop += 1.0

    #updates seat in newhand of player
    def updateSeat(self,seat):
        self.seat = seat
    #returns seat of player

    def getSeat(self):
        return self.seat

    #returns whether a player is playing in a hand or not (bool value)
    def inHand(self):
        return self.playingHand
    def newHand(self,playingHand):
        
        #true unless they're out of the game
        self.playingHand = playingHand
        #reset this to false every new hand (preflop hasn't been called yet)
        self.preFlopCalled = False
        if not playingHand:
            self.updateEliminated()
        else:
            self.handsPlayed +=1.0

    #name of player
    def getName(self):
        return self.name

    #number of times call a bet if not bb or sb (unless raise from blind and call that)
    def preFlopCallOrRaise(self):
        #so as to not double count preflop call 
        if self.preFlopCalled:
            pass
        else:
            self.preFlopCall += 1.0
        self.preFlopCalled = True

    #besides bb and sb, number of times raise/call preflop (if bb or sb raises they count)
    def updateVPIP(self):
        self.VPIP = float(self.preFlopCall) / self.handsPlayed
    def getVPIP(self):
        return self.VPIP

    #WTSD = percentage of hands that went to showdown
    #self.showdown = # of times went to showdown
    def getWTSD(self):
        return self.WTSD
    def updateWTSD(self):
        self.WTSD = float(self.showdown) / self.handsPlayed
        #adds to showdown value (one more showdown counted)
    def showdownAdd(self):   
        self.showdown += 1.0

    #WMSD = percentage of hands won money at showdown (inversely related to WTSD)
    def getWMSD(self):
        return self.WMSD
    def updateWMSD(self):
        self.WMSD = float(self.showdownWin) / self.showdown
    #adds to showdown win value (one more showdown counted)
    def showdownWinAdd(self):   
        self.showdownWin += 1.0

    #PFR = preflop raising
    def getPFR(self):
        return self.PFR
    def updatePFR(self):
        self.PFR = float(self.preFlopRaises) / self.handsPlayed

    def preFlopRaise(self):
        #so as to not double count
        if self.preFlopRaised:
            pass
        else:
            self.preFlopRaises +=1.0
        self.preFlopRaised = True

    #gets aggression factor
    def getAFflop(self):
        return self.AFflop
    def updateAFflop(self):
        if self.totalCallsFlop == 0.0:
            #can't divide by zero, so if calls never made,
            #the af is just the number of aggressive acts done
            self.AFflop = float(self.totalBetRaiseFlop)
        else:
            self.AFflop = float(self.totalBetRaiseFlop) / self.totalCallsFlop

    #gets flop aggression frequency
    def updateAFqFlop(self):
        self.AFq = float(self.totalBetRaiseFlop)/(self.totalBetRaiseFlop + self.totalCallsFlop + self.totalFoldsFlop)

    def getAFqFlop(self):
        return self.AFq

    #total calls increments by one
    def addCallFlop(self):
        self.totalCallsFlop +=1.0
    #total bets/raises increments by one
    def addBetRaiseFlop(self):
        self.totalBetRaiseFlop +=1.0
    #finds player type according to stats
    def findPlayerType(self):
        #higher the player's vpip, the looser the player
        #the lower the player's vpip, the tighter

        #rock if high fold percentage
        #fish 

        #bigger the gap between vpip and pfr, the more often a pleyr cold calls
        #low WTSD means he either folds very often before showdown or he makes opponents fold very often before showdown
        #use WTSD with AF -- if passive and doesn't go to showdown, he's weak tight
        #if aggressive and low wtsd, he makes people fold before showdown very often
        #more than 0.35 WTSD he likes to go to showdown
        #if aggressive and has a high WTSD, then he calls too often with weak hands on the river


        #Mice are even tighter than the rocks, but also very passive.
        #make these suckers fold



        # if self.VPIP <= .08 and self.PFR <= .08 and self.AFflop <= 2:
        #     self.playerType = "MOUSE"
        # #Rocks are very tight, but when they (rarely) see a flop they're after it. Aggressive post flop
        # #make these suckers fold, but know when they have good hands (you should have a better one)
        # elif self.VPIP <= .095 and self.PFR <= .08 and self.AFflop >= 3:
        #     self.playerType = "ROCK"

        #NIT player, combo of mouse and rock
        #VPIP <= 0.13 and self.PFR <= 0.13
        if self.VPIP <= .13 and self.PFR <= .13:
            self.playerType = "NIT"

        #A winning, tight aggressive player.
        #watch out for these.
        #there was a bug, self.PFR was >= 0.6 and self.PFR <=0.13
        elif (self.VPIP >= 0.10 and self.VPIP <= .30) and (self.PFR >= 0.05 and self.PFR <= 0.25) and (self.AFflop >= 2.5 )and (self.WMSD >= .40):
            #TAG player type usually
            self.playerType = "SHARK"

        #Bombs are loose preflop, but also aggressive pre- and postflop.
        elif self.VPIP <= .40 and self.PFR >= .13 and self.AFflop >= 5:        
            self.playerType = "BOMB"

        #Maniacs are very loose and aggressive.
        #generally very loose after flop, go into them if you have something good cuz they will call that shit
        #but you can also lose a lot of money to them early on
        elif self.VPIP >= .35 and self.PFR >= .25 and self.AFq >= .50:
            self.playerType = "MANIAC"

        #They're loose passive and love to call you down.
        #exploit these!
        #their bets and raises are almost never bluffs though/ be careful, don't give them money
        elif self.VPIP >= 0.20 and self.VPIP <= .40 and self.PFR <= 0.15 and self.WTSD >= 0.35 and self.AFflop <= 3:
            self.playerType = "CALLING STATION"
 
        #Cashcows can probably only be found on microlimit. 
        #They're my favorite player class, cause they look at a lot of flops 
        #and even call a lot of preflop raises, but postflop they easily give up their hands.
        #call pfr - 
        #The percentage of hands where the player called a preflop raise when they had the opportunity. This counts all hands where the player faced a preflop raise regardless of any previous or subsequent actions in that hand.
        #Formula:    ( Total Hands Called Pre-Flop Raise / Total Hands Faced Pre-Flop Raise ) * 100
        elif self.VPIP >= .35 and self.PFR >= 0.25 and self.WTSD < .38 and self.AFq <= .50:
            self.playerType = "CASHCOW"
        elif self.AFq >= 0.40 and self.PFR >= 0.13:
            self.playerType = "LOOSE"
        else:
            self.playerType = "UNKNOWN"
            

    #returns the player type/"read"
    def read(self):
        return self.playerType