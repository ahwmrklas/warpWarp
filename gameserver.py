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
# None
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
import math

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
def changePlayerPhase(game, plid, start, finish):
    print("GServer:", plid, " moving from ", start, " to ", finish)
    for player in game['playerList'] :
        if (player['plid'] == plid):
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
def figureStuffOut(logger, game, orders, myShipName, myPower, myTactic, myDrive, myTarget):

    targetShipOrders = findTargetShipOrders(myTarget, orders)
    if (targetShipOrders):
        pretty = dataModel.prettyOrders(targetShipOrders)
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
    logger.log("  " + myShipName + " " + result + " " + myTarget + " for " + str(damage) + " damge")
    print("%s Beam/Missile '%s' %s" % (myShipName, result, myTarget))

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
def resolveCombat(logger, game, orders):
    # For testing
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
            if (not shipOrders):
                print("ERROR:", myShip, "has no orders")
                print("Should assert ... but must fix client")
                continue
            if 'conquer' in shipOrders:
                # This is a change of ownership.
                for baseName in shipOrders['conquer']:
                    logger.log(dataModel.playerNameGet(game, player) + ": conquers " + baseName + " with " + myShip)
                    base = dataModel.findBase(game, baseName)
                    base['owner'] = player
                continue
            pretty = dataModel.prettyOrders(shipOrders)
            logger.log(dataModel.playerNameGet(game, player) + ": " + myShip + ": " + pretty)
            myPower  = shipOrders['beams'][1]
            if (myPower > 0):
                myTactic     = shipOrders['tactic'][0]
                myDrive      = shipOrders['tactic'][1]
                myTarget     = shipOrders['beams'][0]

                figureStuffOut(logger, game, orders, myShip, myPower, myTactic, myDrive, myTarget)

            else:
                # Need ship to deduct missiles
                ship = dataModel.findShip(game, myShip)
                assert(ship)
                for missile in shipOrders['missiles']:
                    myPower  = 2
                    myTactic = 'ATTACK'
                    myDrive  = missile[1]
                    myTarget = missile[0]
                    if (myDrive > 0):
                        assert(ship['M']['cur'] > 0)
                        ship['M']['cur'] -= 1
                        figureStuffOut(logger, game, orders, myShip, myPower, myTactic, myDrive, myTarget)

# PURPOSE:
# RETURNS:
def harvest(game):
    # For now even unowned locations increase BuildPoints every turn
    # That will make unowned locations pile up wealth. Is that good
    # for the game? We could have only "owned" locations do that.
    for star in game['objects']['starList']:
        #un based star BP can only go directly into ship holds
        #We fill up the first ship, and then go on the next
        remaining = star['BP']['perturn']
        for thing in dataModel.findObjectsAt(game, star['location']['x'], star['location']['y']):
            #is this thing a ship?
            if thing['type'] == "ship":
                print(star['name'], " is giving stuff to ", thing['name'])
                #dump stuff in the cargo hold
                oldHauled = thing['Hauled']
                thing['Hauled'] = min([oldHauled + remaining, thing['H']['cur'] * 10])
                remaining -= thing['Hauled'] - oldHauled


        star['BP']['cur'] = star['BP']['cur'] + star['BP']['perturn']
    for thing in game['objects']['starBaseList']:
        thing['BP']['cur'] = thing['BP']['cur'] + thing['BP']['perturn']
    for thing in game['objects']['thingList']:
        thing['BP']['cur'] = thing['BP']['cur'] + thing['BP']['perturn']

# PURPOSE:
# RETURNS: name/plid of winning player or None
def checkForVictory(game):
    # Lots of things could cause you to win
    # (We could even make the victory algorithm selectable?)
    # for now we use the simplest method. If a player owns no bases, they lose.

    # reset victory points to zero
    players = {}
    for player in game['playerList']:
        players[player['plid']] = 0

    for thing in game['objects']['starList']:
        if (thing['owner']):
            players[thing['owner']] = players[thing['owner']] + 1
        print("base: name:", thing['name'], " owner:",thing['owner'])

    #does only one player have a base?
    possibleWinner = None
    for plid, bases in players.items():
        if bases:
            if possibleWinner:
                return None #multiple people have a base. We are still in this!
            else:
                possibleWinner = plid

    #if we get here, only one player has a base!
    #maybe.
    if possibleWinner is None:
        #NO ONE HAS A BASE? panic.
        return "No one"
    else:
        return possibleWinner


# class to handle game commands
class gameserver:

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self):
        self.gameContinues = True
        self.game = dataModel.emptyGame()

        self.seqid = 0

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

    # PURPOSE: Log a history item
    # RETURNS: None
    def log(self, msg):
        if (len(self.game['history']) > 10):
            self.game['history'].pop(0)
        self.game['history'].append({'seqid':self.seqid, 'cmd':msg})
        self.seqid += 1

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
            self.log(dataModel.playerNameGet(self.game, cmd['plid']) + " Ended the game")

            # This cmd doesn't save anything. Call save if you want to save
            self.game['state']['phase'] = None
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
            startingBases = cmd['bases']
            color = cmd['color']

            if int(cmd['plid']) == 0:
                plid = max([0] + [player['plid'] for player in self.game['playerList']]) + 1
            else:
                plid = cmd['plid']

            print("GServer:", "newPlayer", newPlayer)

            player = dataModel.playerTableGet(self.game, plid)

            if player is None:
                self.game['playerList'].append({'name':  newPlayer,
                                                'phase': "creating",
                                                'color': color,
                                                'plid' : plid})
                player = dataModel.playerTableGet(self.game, plid)
                player['color'] = color
                self.log(newPlayer + " is "  + color + " and starts with" + str(startingBases))
                for base in startingBases:
                    ownIt = dataModel.findBase(self.game, base)
                    print(newPlayer, "owns", base)
                    if ownIt:
                        ownIt['owner'] = plid
                        #give them everything at that base
                        baseItems = dataModel.findObjectsAt(self.game, ownIt['location']['x'], ownIt['location']['y'])
                        for baseItem in baseItems:
                            baseItem['owner'] = plid

            else:
                # Normally the player shouldn't exist! But they do for the
                # sample game (or if reconnecting to a game)
                if (player['phase'] is None ):
                    assert( (self.game['state']['phase'] is None) or
                            (self.game['state']['phase'] == "creating")
                          )
                    player['phase'] = "creating"
                    print("GServer: I don't think this should happen anymore")
                else:
                    self.log(newPlayer + " is rejoining game")

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
            self.log(dataModel.playerNameGet(self.game, cmd['plid']) + " Created a new game")
            gameName = cmd['name']
            self.game = dataModel.defaultGame()
            self.game['state']['phase'] = "creating"
            # TODO probably need things like game options???
            # TODO lots of options, right?

        elif cmdStr == 'start':
            # Basically just change state so players can begin building
            # and playing
            self.log("Start command is unused?")
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

            self.log(dataModel.playerNameGet(self.game, cmd['plid']) + " Built the '" + ship['name'] + "' at " + baseName)

            #TODO: This next section is bad. we don't check to see if the player
            #who sent the command owns the base, or is in the right spot.
            #what we should really do is have this command only take the ship,
            #and have the base we work with just be any base on the ship's hex
            #owned by the right player

            #find the base in the game
            base = dataModel.findBase(self.game, baseName)
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
            plid = cmd['plid']
            print("GServer:", "player", plid, "done with phase", self.game['state']['phase'])

            # Based on current phase what do we do?
            if (self.game['state']['phase'] == "creating"):
                # Record ready for given player
                changePlayerPhase(self.game, plid, "creating", "waiting")

                if areAllPlayersInPhase(self.game, "waiting"):
                    self.game['state']['phase'] = "build"
                    changeAllPlayerPhase(self.game, "waiting", "build")

            elif (self.game['state']['phase'] == "build"):
                # Given player can no longer build and must wait
                # When all players ready AUTO move to move phase
                # Record ready for given player
                changePlayerPhase(self.game, plid, "build", "waiting")

                if areAllPlayersInPhase(self.game, "waiting"):
                    self.game['state']['phase'] = "move"
                    changeAllPlayerPhase(self.game, "waiting", "move")
                    # Reset all ships so that can move again
                    for ship in self.game['objects']['shipList']:
                        ship['moves']['cur'] = math.ceil(ship['PD']['cur']/2)

            elif (self.game['state']['phase'] == "move"):
                # Given player can no longer move and must wait
                changePlayerPhase(self.game, plid, "move", "waiting")

                # When all players ready AUTO move to combat phase
                if areAllPlayersInPhase(self.game, "waiting"):
                    self.game['state']['phase'] = "combat"
                    changeAllPlayerPhase(self.game, "waiting", "combat")

            elif (self.game['state']['phase'] == "combat"):
                # Given player finished submitting orders must wait
                changePlayerPhase(self.game, plid, "combat", "waiting")

                # When all players ready AUTO move to ... something
                # damage selection phase if there was combat
                # end turn if there wasn't
                if areAllPlayersInPhase(self.game, "waiting"):
                    if (self.game['orders']):
                        resolveCombat(self, self.game, self.game['orders'])
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
                            self.log("Admiral " + dataModel.playerNameGet(self.game, winner) + " is victorious")
                        else:
                            self.game['state']['phase'] = "build"
                            changeAllPlayerPhase(self.game, "waiting", "build")

                # What if there is no combat? Probably go on to build
                # self.game['state']['phase'] = "build"

            elif (self.game['state']['phase'] == "damageselection"):
                # Given player finished allocating damge to ships
                changePlayerPhase(self.game, plid, "damageselection", "waiting")

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
            
            #the above only works if no warplines are involved
            #if they go to one of these locations, it only costs one
            warpEnds = dataModel.getWarpLineEnd(self.game, ship['location']['x'], ship['location']['y'])
            if [x,y] in warpEnds:
                delta = 1

            print("GServer:", " delta", delta, ship['location']['x'], ship['location']['y'],
                                   x, y)
            #can we actually move this far?
            if (delta <= ship['moves']['cur']):
                self.log(dataModel.playerNameGet(self.game, cmd['plid']) + " Moved the '" + name
                          + "' from (" + str(ship['location']['x']) + "," + str(ship['location']['y'] ) + ")"
                          + " to (" + str(x) + "," + str(y) + ")")
                ship['location']['x'] = x
                ship['location']['y'] = y
                ship['moves']['cur'] = ship['moves']['cur'] - delta

            #are there any system ships stored on this ship?
            #TODO: make sure we don't move too many ships
            for carried_name in ship['carried_ships']:
                #all we have is the name. We need to find the actual ship object in the data model
                carried_ship = dataModel.findShip(self.game, carried_name)
                #update the position of the carried ship
                carried_ship['location']['x'] = x
                carried_ship['location']['y'] = y



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

        elif cmdStr == 'loadship':
            #this is as simple as can be.
            #find both ships, add the name of 1 to the carried list of 2
            ship = dataModel.findShip(self.game, cmd['shipName'])
            mother = dataModel.findShip(self.game, cmd['motherName'])
            #are these guys in the same square
            if ship['location']['x'] == mother['location']['x'] and ship['location']['y'] == mother['location']['y']:
                mother['carried_ships'].append(ship['name'])
                self.log(dataModel.playerNameGet(self.game, cmd['plid'])
                         + " loaded the '" + cmd['shipName'] 
                         + " onto the '" + cmd['motherName'] )

        elif cmdStr == 'unloadship':
            #this is as simple as can be.
            #find the mother, and remove the name of the first ship
            mother = dataModel.findShip(self.game, cmd['motherName'])
            #are these guys in the same square
            mother['carried_ships'].remove(cmd['shipName'])
            self.log(dataModel.playerNameGet(self.game, cmd['plid'])
                         + " unloaded the '" + cmd['shipName'] 
                         + " from the '" + cmd['motherName'] )

        elif cmdStr == 'loadcargo':
            #this is as simple as can be.
            #find both ships, add the name of 1 to the carried list of 2
            ship = dataModel.findShip(self.game, cmd['shipName'])
            star = dataModel.findStarAtLoc(self.game['objects']['starList'], ship['location']['x'], ship['location']['y'])
            shipment = int(cmd['shipment'])
            #are these guys in the same square
            if ship['location']['x'] == star['location']['x'] and ship['location']['y'] == star['location']['y']:
                star['BP']['cur'] -= shipment
                ship['Hauled'] += shipment


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
            print("ship update:", newShip['name'], newShip)
            assert(self.game['state']['phase'] == "damageselection")

            # maybe findShip could return the index too?
            # lookup = dataModel.findShip(self.game, newShip['name'])
            for i, ship in enumerate(self.game['objects']['shipList']) :
                if ship['name'] == newShip['name'] :
                    index = i
                    break

            assert(index is not None)
            if (newShip['damage'] > 0):
                # the damage must have been more than the ship
                # could take; therefore, destroy it.
                self.log("The '" + newShip['name'] + " Exploded!")
                del self.game['objects']['shipList'][index]
            else:
                # Replace existing ship
                self.game['objects']['shipList'][index] = newShip

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
            self.log("savegame isn't implemented")

        elif cmdStr == 'restoregame':
            # Because games are saved/restored on client ...
            # This would do nothing. Just like saveGame
            #
            # Given the name of a file/game.
            # restore that game overwriting the current game
            # Warn/Error if current game hasn't been saved (is dirty)
            print("GServer:", "restoreGame")
            self.log(dataModel.playerNameGet(self.game, cmd['plid']) + " Restored a saved game")
            self.game = cmd['game']

        elif cmdStr == 'listgames':
            # Because games are saved/restored on client ...
            # This would do nothing. Just like saveGame
            #
            # List all of the saved games
            print("GServer:", "listGames")
            self.log("listgames isn't implemented")

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
            self.log("loadgame isn't implemented")

        elif cmdStr == 'playerleave':
            # Player is quiting
            # We could check for permission but I don't think so.
            # This is informational
            # Input? Player name? Some unique player key code for security?
            print("GServer:", "playerLeaving")
            self.log("playerleave isn't implemented")

        else:
            print("GServer:", "Not a legal command '", cmdStr, "'")
            return False

        return True
