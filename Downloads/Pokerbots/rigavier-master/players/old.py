"""    if ev >= 0:
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
                if ev > 10:
                    reply("RAISE", maxBet,s)
                else:
                    reply("RAISE",minBet,s)
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
            reply("FOLD","FOLD",s)"""

"""
    if ev >= 0:
        if ev == 0:
            if "CHECK" in avail_actions:
                reply("CHECK", "CHECK", s)
            elif "CALL" in avail_actions:
                minBet = avail_actions["CALL"][0]
                reply("CALL",minBet,s)

        else:
            action = ""
            minBet = 0
            maxBet = 0
            if "BET" in avail_actions:
                minBet = avail_actions["BET"][0]
                maxBet = avail_actions["BET"][-1]
                #exploit tight players if we have a high ev
                action = "BET"
                reply("BET", minBet,s)
            elif "RAISE" in avail_actions:
                minBet = avail_actions["RAISE"][0]
                maxBet = avail_actions["RAISE"][-1]
                action = "RAISE"
            elif "CALL" in avail_actions:
                minBet = avail_actions["CALL"][0]
                reply("CALL",minBet,s)
            if action == "CALL":
                bets = [minBet]
            else:
                bets = range(minBet,maxBet+1)
            reply(action,bet,s)

    else:
        if "CHECK" in avail_actions:
            reply("CHECK", "CHECK", s)
        else:
            reply("FOLD","FOLD",s)"""