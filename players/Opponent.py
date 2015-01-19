class Opponent:
    def __init__(self,name,stackSize,bb):
        self.name = name
        self.stackSize = stackSize
        self.bb = bb
        self.handID = 1
        self.seat = 0
        self.playingHand = True
        self.eliminated = False

        #type of player
        self.playerType = ""

        ##FOLD PERCENTAGE##
        #percent of times folded preflop
        self.foldPer = 0
        #folds preflop
        self.folds = 0.0

        ##VPIP##
        #percent of times voluntarily put money in pot
        self.VPIP = 0
        self.preFlopCall = 0
        #whether he has already contributed to pot preflop in this hand (so as to not double count preflopCall())
        self.preFlopCalled = False

        ##PFR##
        #preflop raising
        self.PFR = 0       
        #number of times raised preflop
        self.preFlopRaises = 0
        #whether he has already raised preflop (so as to not double count)
        self.preFlopRaised = False
    
        ##WTSD##
        #percent of times went to showdown
        self.WTSD = 0
        #number of showdowns
        self.showdown = 0

        ##WMSD##
        #wmsd is showdown wins percentage
        self.WMSD = 0
        #showdownWin is # of times win at showdown
        self.showdownWin = 0





        




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
    def MRatio(self):
        return self.stackSize / (self.bb + self.bb / 2.0)

    #foldPercentage is % of times fold preflop
    
    #self.playingHand is a bool for whether a player is playing a hand or not
    def foldPercentage(self):
        return self.foldPer
    #foldHandPreflop is number of times fold preflop
    def foldHandPreflop(self):
        self.folds+= 1.0
        self.fold()
        self.updateFoldPer()
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
        #reset this to false every new hand (preflop hasn't been called yet)
        self.preFlopCalled = False
        if not playingHand:
            self.updateEliminated()

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

    def preFlopRaise(self):
        #so as to not double count
        if self.preFlopRaised:
            pass
        else:
            self.preFlopRaises +=1
        self.preFlopRaised = True


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
            
        
        
    
        
                     