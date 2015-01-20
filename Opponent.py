class Opponent:
    def __init__(self,name,stackSize,bb):
        self.name = name
        self.stackSize = stackSize
        self.bb = bb
        #hands played (not counting when eliminated), not just handID
        self.handsPlayed = 0.0
        self.seat = 0.0
        self.playingHand = True
        self.eliminated = False

        #type of player
        self.playerType = ""

        ##FOLD PERCENTAGE##
        #percent of times folded preflop
        self.foldPer = 0.0
        #folds preflop
        self.foldsPreFlop = 0.0

        #total folds
        self.totalFolds = 0

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

        ##AGGRESSION FACTOR##
        #AF is percentage of time (bet + raise)/calls
        self.AF = 0.0
        self.totalCalls = 0.0
        self.totalBetRaise = 0.0

        #FLOP AGGRESION FREQUENCY
        self.AFq = 0

        #M ratio
        self.M = 0.0

    #updates stack value of player
    def updateStack(self,stack):
        self.stackSize = stack   
    #retrieves stacksize of player     
    def getStack(self):
        return self.stackSize

    #updates whether eliminated or not
    def updateEliminated(self):
        #if eliminated this becomes true
        self.eliminated = True

    #whether the player is eliminated from tournament or not
    def isEliminated(self):
        return self.eliminated

    #m ratio of players (this affects play)
    def updateMRatio(self):
        self.M = self.stackSize / (self.bb + self.bb / 2.0)
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
        self.foldPer = (float(self.folds) / self.handsPlayed)
    #for any fold (not just preflop like foldHand, playingHand goes to false)
    def fold(self):
        self.playingHand = False
        self.totalFolds += 1

    #updates seat in newhand of player
    def updateSeat(self,seat):
        self.seat = seat
    #returns seat of player

    def seat(self):
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
            self.handsPlayed +=1

    #name of player
    def getName(self):
        return self.name

    #number of times call a bet if not bb or sb (unless raise from blind and call that)
    def preFlopCallOrRaise(self):
        #so as to not double count preflop call 
        if self.preFlopCalled:
            pass
        else:
            self.preFlopCall += 1
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
        self.showdown += 1

    #WMSD = percentage of hands won money at showdown (inversely related to WTSD)
    def getWMSD(self):
        return self.WMSD
    def updateWMSD(self):
        self.WMSD = float(self.showdownWin) / self.handsPlayed
    #adds to showdown win value (one more showdown counted)
    def showdownWinAdd(self):   
        self.showdownWin += 1

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
            self.preFlopRaises +=1
        self.preFlopRaised = True

    #gets aggression factor
    def getAF(self):
        return self.AF
    def updateAF(self):
        if self.totalCalls == 0:
            #can't divide by zero, so if calls never made,
            #the af is just the number of aggressive acts done
            self.AF = float(self.totalBetRaise)
        else:
            self.AF = float(self.totalBetRaise) / self.totalCalls

    #gets flop aggresion frequency
    def updateAFq(self):
        self.AFq = self.totalBetRaise/(self.totalBetRaise + self.totalCalls + self.totalFolds)

    def getAFq(self):
        return self.AFq

    #total calls increments by one
    def addCall(self):
        self.totalCalls +=1
    #total bets/raises increments by one
    def addBetRaise(self):
        self.totalBetRaise +=1
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

        if self.VPIP <= .08 and self.PFR <= .08 and self.AF <= 2:
            self.playerType = "MOUSE"
        elif self.VPIP <= .095 and self.PFR <= .08 and self.AF >= 3:
            self.playerType = "ROCK"
        elif self.VPIP <= .22 and self.VPIP >= .15 and self.PFR/self.VPIP >= .7 and self.AF >= 3 and self.WMSD >= .50:
            self.playerType = "SHARK"
        elif self.VPIP <= .25 and self.PFR >= .13 and self.AF >= 5:
            self.playerType = "BOMB"
        elif self.VPIP >= 20 and self.VPIP <= .30 and self.PFR <= 10 and self.WTSD >= 33 and self.AF <= 2.5:
            self.playerType = "CALLING STATION"
        elif self.VPIP >= .35 and self.PFR >= .25 and self.AFq >= .50:
            self.playerType = "MANIAC"
        elif self.VPIP >= .39 and self.PFR >= 30 and self.WTSD < .30 and self.AFq <= .50:
            self.playerType = "CASHCOW"
        else:
            self.playerType = "UNKNOWN"
        return self.playerType

    #returns the player type/"read"
    def read(self):
        return self.playerType