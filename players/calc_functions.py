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

def foldBet():
    

    if "BET" in avail_actions:
        minBet = avail_actions["BET"][0]
        maxBet = avail_actions["BET"][-1]
    elif "RAISE" in avail_actions:
        minBet = avail_actions["RAISE"][0]
        maxBet = avail_actions["RAISE"][-1]
    
    
    

def estimatedValue(equities,pot_size,bet):
    ourEquity = equities.ev[0]
    theirEquity = equities.ev[1]       
    winAmt = pot_size + bet
    loseAmt =  bet
    estimated_value = ourEquity * winAmt - (1.0-ourEquity) * loseAmt
    
    return estimated_value

def impliedOdds(equities,pot_size,bet):
    ourEquity = equities.ev[0]
    x = float(bet) / ourEquity
    y = pot_size + bet + bet
    impliedOdds = x - y
    return impliedOdds
