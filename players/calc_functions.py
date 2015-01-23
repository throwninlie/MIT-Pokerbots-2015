import pbots_calc


def equityCalculator(holeCard1,holeCard2,board,iterations,theirCards = None, dead= None):
    if theirCards == None:
        theirCards = "xx"
    if board == "":
        pass
    else:
        board = ''.join(board)
    #print theirCards
    
    if dead == None:
        dead = ""
        r= ""
    word = holeCard1+holeCard2+":"+theirCards
    
    equities = pbots_calc.calc(word,board,dead,iterations)
    return equities

def foldEquity(pot,ev,foldPercentage1,foldPercentage2 = None):
    foldEquities = []
    #should we just take into account folds preflop, or total folds?
    opp1Fold = pot*foldPercentage1 + (1.0-float(foldPercentage1))*ev
    foldEquities.append(opp1Fold)
    if foldPercentage2 is not None:
        opp2Fold = pot*foldPercentage2 + (1.0-float(foldPercentage2))*ev
        foldEquities.append(opp2Fold)       
    return foldEquities
    
def expectedValue(equities,pot_size,bet):
    ourEquity = equities.ev[0]
    theirEquity = equities.ev[1]       
    winAmt = pot_size
    loseAmt =  bet
    estimated_value = ourEquity * winAmt - (1.0-ourEquity) * loseAmt
    return estimated_value

def potOdds(pot_size,bet):
    return float(bet)/pot_size
def impliedOdds(equities,pot_size,bet):
    ourEquity = equities.ev[0]
    if ourEquity == 0.0:
        x = 10000
    else:
        x = float(bet) / ourEquity
    y = pot_size + bet + bet
    impliedOdds = x - y
    return impliedOdds
def potOdds(pot_size,bet):
    #bet / pot, not 1- bet/pot
    return (float(bet) / pot_size)
def maxBetEV(pot_size,equity,our_bot_stack):
    if equity == 1.0:
        maxBet = 1000
    else:
        maxBet = (float(pot_size)* equity)/ (1.0 - equity)
    return int(maxBet)
def foldPercentageNeeded(pot_size,bet,equity):
        num = -2.0 * bet * equity + bet - pot_size*equity
        denom = -2.0 * bet * equity + bet - pot*equity + pot
        return float(num) / denom
def foldBet(foldPercentage, pot_size,our_bot_stack):
    if foldPercentage == 1.0:
        maxBetFold = our_bot_stack
    else:
        maxBetFold = (foldPercentage * pot_size )/ (1.0 - foldPercentage)
    return int(maxBetFold)

