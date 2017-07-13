# class to handle game commands
# Game state goes from:
# Nil
# Game created and ready for players
# Players join? Select starting locations?
# Building phase,
# Check finished building, Waiting for other players to finish building
# Movement phase,
# Check finished movement, wait for other players to finish moving
# Combat phase
#   Choose battles? Battles chosen
#   Make combat plans,
#   submit combat plans, wait for oppoent to finish combat plans
#   Results of battle reported
#   Select damage,
#   submit damage selection, wait for opponent to finish damage selections
#   All battles finished? On to next battle.
#
# Done? Back to Build phase
#
#
# PHASE:
# nil
# creating
# build
# move
# combat
# battle
# damageselection
# Official rules have "SystemShipRearrangement". Drop this. It seems redundant
# victory


import sys
sys.path.append("/home/ahw/views/warpWar/test")

import json
import ijk
import dataModel

# PURPOSE: look up base name in game base & star list
# RETURNS: entry of base
def findBase(game, baseName):
    for base in game['objects']['starBaseList']:
        if base['name'] == baseName:
            return base
    for base in game['objects']['starList']:
        if base['name'] == baseName:
            return base
    return None

# PURPOSE: look to see if all players are in a given phase
# RETURNS: true iff all players in game are in phase
def areAllPlayersInPhase(game, phase):
    #check to see if all players are in a given phase
    for player in game['playerList'] :
        if (player['phase'] != phase):
            return False
    return True

# PURPOSE: Change given player from startphase to finishphase
# RETURNS: true if successfully moved
def changePlayerPhase(game, playerName, start, finish):
    print("GServer:", playerName, " moving from ", start, " to ", finish)
    for player in game['playerList'] :
        if (player['name'] == playerName):
            assert(player['phase'] == start)
            player['phase'] = finish
            return True

    return False

# PURPOSE: Change All players from startphase to finishphase
# I think this will only be used to change *out* of "waiting"
# RETURNS: true if successfully moved
def changeAllPlayerPhase(game, start, finish):
    print("GServer:", "moving ALL from ", start, " to ", finish)
    for player in game['playerList'] :
        assert(player['phase'] == start)
        player['phase'] = finish

    return True

# PURPOSE:
# RETURNS: string representation of given order
def prettyOrders(order):
    tactic = order['tactic'][0]
    drive  = order['tactic'][1]
    beamTarget  = order['beams'][0]
    beamPower   = order['beams'][1]
    screenPower = order['screens']
    pretty = "%s: D=%d, B=(%d, %s), S=%d" % (tactic, drive, beamPower, beamTarget, screenPower)
    missiles = ""
    for missile in order['missiles']:
        missiles += "\nT=(%d, %s)" % (missile[1], missile[0])

    return pretty + missiles

# PURPOSE:
# RETURNS:
def combatChartLookup(myTactic, myDrive, targetTactic, targetDrive):
    combatChart = {
        'ATTACK': {
            'ATTACK': {
                -4:'Miss',
                -3:'Miss',
                -2:'Hit',
                -1:'Hit',
                 0:'Hit+2',
                 1:'Hit+2',
                 2:'Hit+1',
                 3:'Miss',
                 4:'Miss',
                 5:'Miss',
            },
            'DODGE': {
                -4:'Miss',
                -3:'Miss',
                -2:'Miss',
                -1:'Miss',
                 0:'Miss',
                 1:'Miss',
                 2:'Hit+1',
                 3:'Hit',
                 4:'Hit',
                 5:'Miss',
            },
            'RETREAT': {
                -4:'Escapes',
                -3:'Escapes',
                -2:'Escapes',
                -1:'Escapes',
                 0:'Miss',
                 1:'Miss',
                 2:'Miss',
                 3:'Hit',
                 4:'Hit',
                 5:'Miss',
            },
        },
        'DODGE': {
            'ATTACK': {
                -4:'Miss',
                -3:'Miss',
                -2:'Miss',
                -1:'Hit',
                 0:'Hit',
                 1:'Hit',
                 2:'Hit',
                 3:'Miss',
                 4:'Miss',
                 5:'Miss',
            },
            'DODGE': {
                -4:'Miss',
                -3:'Hit',
                -2:'Hit',
                -1:'Hit',
                 0:'Hit',
                 1:'Miss',
                 2:'Miss',
                 3:'Miss',
                 4:'Miss',
                 5:'Miss',
            },
            'RETREAT': {
                -4:'Escapes',
                -3:'Escapes',
                -2:'Escapes',
                -1:'Escapes',
                 0:'Escapes',
                 1:'Escapes',
                 2:'Escapes',
                 3:'Escapes',
                 4:'Escapes',
                 5:'Escapes',
            },
        },
        'RETREAT': {
            'ATTACK': {
                -4:'Miss',
                -3:'Miss',
                -2:'Miss',
                -1:'Hit',
                 0:'Hit',
                 1:'Miss',
                 2:'Miss',
                 3:'Miss',
                 4:'Miss',
                 5:'Miss',
            },
            'DODGE': {
                -4:'Miss',
                -3:'Miss',
                -2:'Miss',
                -1:'Miss',
                 0:'Miss',
                 1:'Miss',
                 2:'Miss',
                 3:'Miss',
                 4:'Miss',
                 5:'Miss',
            },
            'RETREAT': {
                -4:'Escapes',
                -3:'Escapes',
                -2:'Escapes',
                -1:'Escapes',
                 0:'Escapes',
                 1:'Escapes',
                 2:'Escapes',
                 3:'Escapes',
                 4:'Escapes',
                 5:'Escapes',
            },
        },
    }

    # (myTactic, myDrive, targetTactic, targetDrive):
    # The lookup tables range from -4 to +5 so
    # limit the range
    driveDiff = myDrive - targetDrive
    if (driveDiff < -4):
        driveDiff = -4
    elif (driveDiff > 5):
        driveDiff = 5

    result = combatChart[myTactic][targetTactic][driveDiff]
    return result

# PURPOSE:
# RETURNS:
def findTargetShipOrders(shipName, orders):
    for player, playerOrders in orders.items():
        for ship, shipOrders, in playerOrders.items():
            if (shipName == ship):
                return shipOrders
    return None

# PURPOSE:
# RETURNS:
# passing in "game" and "orders" seems overkill. Just pass in game
# and find the orders ... buy that also seems weird
def figureStuffOut(game, orders, myShipName, myPower, myTactic, myDrive, myTarget):

    targetShipOrders = findTargetShipOrders(myTarget, orders)
    if (targetShipOrders):
        pretty = prettyOrders(targetShipOrders)
        print("targetship:", myTarget, "order:", pretty)
        targetTactic     = targetShipOrders['tactic'][0]
        targetDrive      = targetShipOrders['tactic'][1]
        targetScreen     = targetShipOrders['screens']
    else:
        # Can't find otders for the target.
        # That shouldn't happen. assert?
        # Maybe the target player was just lazy?
        # ??? This should be considered an error on the part
        # of the client.
        print("targetship:", myTarget, "CAN'T FIND ORDERS!!!!")
        targetTactic     = 'RETREAT'
        targetDrive      = 0
        targetScreen     = 0

    # We know what the offense is doing, we know what the defense is doing
    # rock, paper, scissors the results
    result = combatChartLookup(myTactic, myDrive, targetTactic, targetDrive)
    print("%s Beam/Missile '%s' %s" % (myShipName, result, myTarget))

    # ugly if statement on results
    # combatChartLookup should probably just return the number
    if   result == "Miss":
        damage = 0
    elif result == "Hit":
        damage = 0 + myPower
    elif result == "Hit+1":
        damage = 1 + myPower
    elif result == "Hit+2":
        damage = 2 + myPower
    elif result == "Escapes":
        damage = -1
    else:
        print('ERROR!')

    # A negative number means the target
    # has escaped. BUT it can't escape unless EVERY attack results in "escape"
    if (damage < 0):
        return

    # Target didn't escape but has the screen protected it?
    if (damage < targetScreen):
        damage = 0
    else:
        damage -= targetScreen

    targetShip = dataModel.findShip(game, myTarget)
    # This is a worse error on the part of the client
    #assert(targetShip)
    if (targetShip is None):
        print("targetship:", myTarget, "CAN'T FIND SHIP!!!!")
        return

    # Note I was going to have a negative damage mean
    # the ship escaped

    # This damage calculation is incorrect.
    # Lookup the rules and the screens only protect you from
    # the TOTAL number of hits in the round. So a whole bunch
    # of "1" damage can overcome the shields eventually.

    if (targetShip['damage'] < 0) and (damage >=0):
        targetShip['damage'] = 0

    targetShip['damage'] += damage

# PURPOSE:
# RETURNS:
def resolveCombat(game, orders):
    # FIXME:
    # for now cycle through every ship in combat and give it
    # some points of damage ... eh, just damage all ships :-)
    #for ship in game['objects']['shipList']:
    #    ship['damage'] = 5

    print("ALLorders:")
    print(orders)

    # What are the combat orders?
    # Find each combat order.
    # Find target of each order (an order can have multiple targets)
    # Find the orders for each target.
    # Match them up and resolve - so I need a simple function
    # for one v one orders to resolve against the chart

    # Table of orders is:
    # Array of players (dict)
    #    For each player there is an array of ships (dict)
    #       For each ship there is an order
    #           each order can have a unique target
    for player, playerOrders in orders.items():
        for myShip, shipOrders, in playerOrders.items():
            pretty = prettyOrders(shipOrders)
            print(player, "ship:", myShip, "order:", pretty)
            myPower  = shipOrders['beams'][1]
            if (myPower > 0):
                myTactic     = shipOrders['tactic'][0]
                myDrive      = shipOrders['tactic'][1]
                myTarget     = shipOrders['beams'][0]

                figureStuffOut(game, orders, myShip, myPower, myTactic, myDrive, myTarget)

            else:
                for missile in shipOrders['missiles']:
                    myPower  = 2
                    myTactic = 'ATTACK'
                    myDrive  = missile[1]
                    myTarget = missile[0]
                    figureStuffOut(game, orders, myShip, myPower, myTactic, myDrive, myTarget)

# PURPOSE:
# RETURNS:
def harvest(game):
    # For now event unowned locations increase BuildPoints every turn
    # That will make unowned locations pile up wealth. Is that good
    # for the game? We could have only "owned" locations do that.
    for thing in game['objects']['starList']:
        thing['BP']['cur'] = thing['BP']['cur'] + thing['BP']['perturn']
    for thing in game['objects']['starBaseList']:
        thing['BP']['cur'] = thing['BP']['cur'] + thing['BP']['perturn']
    for thing in game['objects']['thingList']:
        thing['BP']['cur'] = thing['BP']['cur'] + thing['BP']['perturn']

# PURPOSE:
# RETURNS: name/plid of winning player or None
def checkForVictory(game):
    # Lots of things could cause you to win
    # (We could even make the victory algorithm selectable?)
    # For now just the person with the largest owned build points
    # over a given threshold

    # reset victory points to zero
    players = {}
    players['none'] = 0
    for player in game['playerList']:
        players[player['name']] = 0

    for thing in game['objects']['starList']:
        players[thing['owner']] = players[thing['owner']] + thing['BP']['cur']
        print("star: name:", thing['name'], " owner:",thing['owner'])
    for thing in game['objects']['starBaseList']:
        players[thing['owner']] = players[thing['owner']] + thing['BP']['cur']
        print("base: name:", thing['name'], " owner:",thing['owner'])
    for thing in game['objects']['thingList']:
        players[thing['owner']] = players[thing['owner']] + thing['BP']['cur']
        print("thing: name:", thing['name'], " owner:",thing['owner'])

    # Check everyones victory points. Did anyone win?
    highest = 0
    for name, score in players.items():
        print("name:", name, " score:", score)
        if (score > highest):
            highest = score
            winner = name

    if (highest > 30):
        return winner

    return None


# class to handle game commands
class gameserver:

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self):
        self.gameContinues = True
        self.game = dataModel.emptyGame()

        # This is used for debug
        self.cmdStr = None

    # PURPOSE: Have we received the quit command
    # RETURNS: true if no quit command yet
    def gameOn(self):
        return self.gameContinues

    # PURPOSE: Return the JSON representing the entire game
    # RETURNS: game state as a JSON string
    def gameJson(self):
        return json.dumps(self.game, ensure_ascii=False)

    # PURPOSE: Interpret JSON command and do something
    # RETURNS: true for properly parsed command
    def parseCmd(self, jsonStr):
        try:
            root = json.loads(jsonStr)
        except Exception as error:
            print("GServer:", "JSON parse error for ", jsonStr, "\n")
            return False

        cmd = root['cmd']
        cmdStr = cmd['cmd']
        if (self.cmdStr != cmdStr):
            print("GServer: (%s) CMD: %s PHASE: %s" % (cmd['plid'], cmdStr, self.game['state']['phase']))
        self.cmdStr = cmdStr

        if cmdStr == 'quit':
            print("GServer:", "quitCommandRecieved")

            # This cmd doesn't save anything. Call save if you want to save
            self.game['state']['phase'] = "nil"
            self.gameContinues = False

        elif cmdStr == 'ping':
            # simple test to see if server responds. So print and respond
            # print("GServer:", "ping")
            pass

        elif cmdStr == 'newplayer':
            # New player requests to join.
            # I guess we would look at the game state? Hmmm
            # What about a player joining a previously saved game?
            # Input? Player name and potentially player specific options
            # What player specific options? IP:port?
            newPlayer = cmd['name']
            print("GServer:", "newPlayer", newPlayer)

            player = dataModel.playerTableGet(self.game, newPlayer)

            if player is None:
                self.game['playerList'].append({'name':  newPlayer,
                                                'phase': "creating"})
            else:
                # Normally the player shouldn't exist! But they do for the
                # sample game (or if reconnecting to a game)
                if (player['phase'] == "nil"):
                    assert( (self.game['state']['phase'] == "nil") or
                            (self.game['state']['phase'] == "creating")
                          )
                    player['phase'] = "creating"
                else:
                    print("GServer:", "player", player, "must be rejoining game???!!!")

        elif cmdStr == 'newgame':
            # What to do? Offer to save current game? NO! this is the server,
            # do as commanded
            # erase current game/dictionary
            # Start empty
            # Input? Would be list of options for game
            # Should we prevent this? Perhaps block it? Only permit it
            # if there is only one connected player?
            #
            # Need to be given the name of the game?
            # Warn/Error if current game hasn't been saved (is dirty)
            gameName = cmd['name']
            self.game = dataModel.emptyGame()
            assert(self.game['state']['phase'] == "nil")
            self.game['state']['phase'] = "creating"
            # TODO probably need things like game options???
            # TODO lots of options, right?

        elif cmdStr == 'start':
            # Basically just change state so players can begin building
            # and playing
            assert(self.game['state']['phase'] == "creating")
            self.game['state']['phase'] = "build"

        elif cmdStr == 'buildship':
            # Now we get to fun stuff
            # Check for proper state to see if player permitted to build.
            # Validate a legal build. Does player have the money?
            # Input? ... this is a lot... The entire ship? We would have
            # to calculate the cost based on the options and validate it.
            # We would have to deduct the cost from the players total.
            # Of course need to see if it is a valid ship to begin with
            # TODO lots of parameters!
            ship = cmd['ship']
            baseName = cmd['base']
            assert(self.game['state']['phase'] == "build")

            #lets do this the lazy way first. just append the ship to the list!
            print("GServer:", "ship to append:")
            print(ship)
            #How much will this ship cost?
            cost = 0
            cost += ship['PD']['max']
            cost += ship['B']['max']
            cost += ship['S']['max']
            cost += ship['E']['max']
            cost += ship['T']['max']
            cost += ship['M']['max'] / 3
            cost += ship['A']['max'] / 2
            cost += ship['C']['max']
            cost += ship['SH']['max'] / 6
            cost += ship['SR']['max']
            cost += ship['H']['max']
            cost += ship['R']['max'] * 5
            if ship['WG']['max'] == True:
                cost += 5

            print ("GServer cost:", cost)

            #TODO: This next section is bad. we don't check to see if the player
            #who sent the command owns the base, or is in the right spot.
            #what we should really do is have this command only take the ship,
            #and have the base we work with just be any base on the ship's hex
            #owned by the right player

            #find the base in the game
            base = findBase(self.game, baseName)
            if (base is not None):
                #does the base have enough to pay for the ship?
                if base['BP']['cur'] >= cost:
                    #subtract the cost...
                    print (base)
                    base['BP']['cur'] -= cost
                    print (base)
                    #and build the ship!
                    self.game['objects']['shipList'].append(ship)

        elif cmdStr == 'ready':
            # A generic cmd used to end several phases
            playerName = cmd['name']
            print("GServer:", "player", playerName, "done with phase", self.game['state']['phase'])

            # Based on current phase what do we do?
            if (self.game['state']['phase'] == "creating"):
                # Record ready for given player
                changePlayerPhase(self.game, playerName, "creating", "waiting")

                if areAllPlayersInPhase(self.game, "waiting"):
                    self.game['state']['phase'] = "build"
                    changeAllPlayerPhase(self.game, "waiting", "build")

            elif (self.game['state']['phase'] == "build"):
                # Given player can no longer build and must wait
                # When all players ready AUTO move to move phase
                # Record ready for given player
                changePlayerPhase(self.game, playerName, "build", "waiting")

                if areAllPlayersInPhase(self.game, "waiting"):
                    self.game['state']['phase'] = "move"
                    changeAllPlayerPhase(self.game, "waiting", "move")

            elif (self.game['state']['phase'] == "move"):
                # Given player can no longer move and must wait
                changePlayerPhase(self.game, playerName, "move", "waiting")

                # When all players ready AUTO move to combat phase
                if areAllPlayersInPhase(self.game, "waiting"):
                    self.game['state']['phase'] = "combat"
                    changeAllPlayerPhase(self.game, "waiting", "combat")

            elif (self.game['state']['phase'] == "combat"):
                # Given player finished submitting orders must wait
                changePlayerPhase(self.game, playerName, "combat", "waiting")

                # When all players ready AUTO move to ... something
                # damage selection phase if there was combat
                # end turn if there wasn't
                if areAllPlayersInPhase(self.game, "waiting"):
                    if (self.game['orders']):
                        resolveCombat(self.game, self.game['orders'])
                        self.game['state']['phase'] = "damageselection"
                        changeAllPlayerPhase(self.game, "waiting", "damageselection")
                    else:
                        # Skip "SystemShipRearrangement"
                        # Start turn sequence over again
                        # Collect build points, Check victory conditions

                        harvest(self.game)

                        winner = checkForVictory(self.game)
                        if (winner):
                            self.game['state']['phase'] = "victory"
                            changeAllPlayerPhase(self.game, "waiting", "loser")
                            changePlayerPhase(self.game, winner, "loser", "winner")
                        else:
                            self.game['state']['phase'] = "build"
                            changeAllPlayerPhase(self.game, "waiting", "build")

                # What if there is no combat? Probably go on to build
                # self.game['state']['phase'] = "build"

            elif (self.game['state']['phase'] == "damageselection"):
                # Given player finished allocating damge to ships
                changePlayerPhase(self.game, playerName, "damageselection", "waiting")

                # When all players ready AUTO move to the next round of combat
                if areAllPlayersInPhase(self.game, "waiting"):
                    self.game['state']['phase'] = "combat"
                    changeAllPlayerPhase(self.game, "waiting", "combat")

                    # Erase any existing orders. They no longer have any use
                    self.game['orders'] = {}

            # UNUSED? FIXME
            elif (self.game['state']['phase'] == "battle"):
                # Given player can no longer give orders and must wait
                # When all players ready AUTO move to damageSelection phase
                # or resolve combat phase? Is there such a phase?
                self.game['state']['phase'] = "damageselection"
            else:
                print("GServer:", "Invalid phase for 'ready'")
                assert(False)

        elif cmdStr == 'moveship':
            # Input? ShipID, new location of ship? Movement vector?
            # Is it legal to move? (Proper turn sequence. Valid location on
            # map? Currently in combat? Does move cause combat? (meaning ship
            # halts immediately))
            # Deduct movement from ship
            name = cmd['name']
            x = cmd['x']
            y = cmd['y']

            assert(self.game['state']['phase'] == "move")

            ship = dataModel.findShip(self.game, name)
            if (ship is None):
                print("GServer:", "error: Ship not found", name)
                return False

            si,sj,sk = ijk.XYtoIJK(x, y)
            fi,fj,fk = ijk.XYtoIJK(ship['location']['x'], ship['location']['y'])
            delta = int((abs(si-fi) + abs(sj-fj) + abs(sk-fk)) / 2)

            print("GServer:", " delta", delta, ship['location']['x'], ship['location']['y'],
                                   x, y)
            ship['location']['x'] = x
            ship['location']['y'] = y
            ship['moves']['cur'] = ship['moves']['cur'] -delta 

            #now we start a battle, if we can.
            #Is there anything here that can trigger a battle?
            for otherShip in self.game['objects']['shipList']:
                if otherShip['name'] != name:
                    if otherShip['location']['x'] == x and otherShip['location']['y'] == y:
                        if otherShip['owner'] != ship['owner']:
                            ship['moves']['cur'] = 0
                            #if we want wierd simultaneous movement, both ships stop
                            otherShip['moves']['cur'] = 0
                            #set a flag, or have everyone else figure it out for themselves?

        elif cmdStr == 'combatorders': # Per ship? All ships?
            # A combat instruction
            # Check for proper state. Are there existing orders?
            # Have all ships in combat been given orders?
            # Have all opponents ships in *this* combat been given orders?
            # Input? ShipID, combat command (fire, move, shields ...)
            # TODO many more parameters

            plid = cmd['plid']
            battleOrders = cmd['battleOrders']
            print("battleOrders:", battleOrders)

            assert(self.game['state']['phase'] == "combat")

            #Every player gives a list of orders, for all ships involved in a
            #Conflict. Once both players have sent orders, we start processing.

            self.game['orders'][plid] = battleOrders

            # When all players ready (have submitted orders)
            # AUTO move to damageselection phase
            # When all damage has been selected ... by all players ...
            # move to battle .... or retreat ... or combat over ... or next
            # battle?

        elif cmdStr == 'acceptdamage':
            # Deduct combat damage
            # Input? ShipID, damage deducted from each component
            # Did they deduct enough damage?
            # Do they have more ships with damage to deduct?
            # TODO many more parameters
            # A ship that has been destroyed should be removed
            # (perhaps moved to a "dead" list)

            plid = cmd['plid']
            newShip = cmd['ship']
            print("ship update:", newShip)
            assert(self.game['state']['phase'] == "damageselection")

            # maybe findShip could return the index too?
            # dataModel.findShip(self.game, newShip['name'])
            for index, ship in enumerate(self.game['objects']['shipList']) :
                if ship['name'] == newShip['name'] :
                    self.game['objects']['shipList'][index] = newShip
                    break

        elif cmdStr == 'savegame':
            # Write file ... who is responsible for game save?
            # I Don't want to load/restore game that is stored on the server
            # ... well, I would like to but that API would be a pain.
            # I'd have to do all the directory I/O work. Remember the game
            # server has no UI. So I would read files and directories
            # off of the server and then let the client navigate, select and
            # choose save/load
            #
            # Given a file name write that file to some save location
            # Mark the game as saved (not dirty)
            # It is possible that the name of the game (name of the file)
            # is already part of the game so you wouldn't need to provide
            # the name.
            #
            # Server does nothing with saveGame. The client must save the game
            print("GServer:", "saveGame")

        elif cmdStr == 'restoregame':
            # Because games are saved/restored on client ...
            # This would do nothing. Just like saveGame
            #
            # Given the name of a file/game.
            # restore that game overwriting the current game
            # Warn/Error if current game hasn't been saved (is dirty)
            print("GServer:", "restoreGame")
            self.game = cmd['game']

        elif cmdStr == 'listgames':
            # Because games are saved/restored on client ...
            # This would do nothing. Just like saveGame
            #
            # List all of the saved games
            print("GServer:", "listGames")

        elif cmdStr == 'loadgame':
            # Offer to save current game?
            # Bring up selection dialog
            # load game overwriting existing game
            #
            # Like, newGame check for permission.
            # Input? Would be an entire JSON game
            # We should probably do some kind of validation but
            # this would just be pulling in the JSON and
            # translating it to the dict.
            #
            # Warn/Error if current game hasn't been saved (is dirty)
            print("GServer:", "loadGame")

        elif cmdStr == 'playerleave':
            # Player is quiting
            # We could check for permission but I don't think so.
            # This is informational
            # Input? Player name? Some unique player key code for security?
            print("GServer:", "playerLeaving")

        else:
            print("GServer:", "Not a legal command '", cmdStr, "'")
            return False

        return True
