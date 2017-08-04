from samplegame import sampleGame
import copy
#Purpose: find the difference between two dictionaries
#Returns: A dict which includes:
#           new keys, with the values
#           keys whose values have changed
#        Does NOT include:
#           keys which are not present in the new dict
def dictDiff(old,new):
    #get a list of keys from both, and see which are new
    oldKeys = [key for key in old.keys()]
    newKeys = [key for key in new.keys()]
    diffKeys = [key for key in newKeys if key not in oldKeys]
    sameKeys = [key for key in newKeys if key not in diffKeys]
    diffDict = {}
    for key in sameKeys:
        #are the values different?
        if old[key] != new[key]:
            diffDict[key] = new[key]
        #else:
            #this gets tricky. if its a dictionary, recurse.
            #if type(new[key]) is dict:
                #if dictDiff(old[key],new[key]):
                    #diffDict[key] = new[key]

    for key in diffKeys:
        diffDict[key] = new[key]

    return diffDict

def gameDiff(oldGame,newGame):
    if not oldGame:
        return newGame
    diff = [{},{}]
    for key in newGame.keys():
        if key == 'objects':
            if oldGame[key] != newGame[key]:
                for objectkey in newGame[key]:
                    toDelete = []
                    toAdd = []
                    if oldGame[key][objectkey] == newGame[key][objectkey]:
                        continue
                    for i in range(len(oldGame[key][objectkey])):
                        if oldGame[key][objectkey][i] not in newGame[key][objectkey]:
                            toDelete.append(i)
                    for i in range(len(newGame[key][objectkey])):
                        if newGame[key][objectkey][i] not in oldGame[key][objectkey]:
                            toAdd.append( newGame[key][objectkey][i])
                    diff[1][objectkey] = (toDelete,toAdd)
                            

        elif oldGame[key] != newGame[key]:
            diff[0][key] = newGame[key]
    return diff

#Purpose: recursively hunt down what changed
#returns: a list tuple of the list of keys/indexes, and the new value
def gameDiffHelper(oldPiece, newPiece):
    #The base case: a value has been changed, an entry has been added, or removed.
    #what are we. we can't be none
    if oldPiece is None or newPiece is None:
        return None
    assert(oldPiece != newPiece)
    pieceType = type(oldPiece)
    assert(pieceType == type(newPiece))
    diffList = []
    #are we a list or a dict?
    if pieceType == dict:
        #make sure we don't need to recurse
        for key in set(oldPiece.keys()) | set(newPiece.keys()):
            if key not in oldPiece.keys():
                #we created something new!
                diffList.append ((key,newPiece[key]))
            if key not in newPiece.keys():
                #something was lost!
                diffList.append (([key],None))
            #okay, so the key is in both dicts.
            if newPiece[key] == oldPiece[key]:
                continue
            #so the key is present, but there is a difference in the value
            if type(newPiece[key]) in (list, dict):
                #we recurse on lists or dicts
                recurseResult = gameDiffHelper(oldPiece[key], newPiece[key])
                for result in recurseResult:
                    diffList.append(([key, *result[0]], result[1]))
            else:
                #sweet, we found a base case
                diffList.append([key], newPiece[key])

    elif pieceType == list:
        #Go through every item once
        #keep track of the offset
        change = 0
        for i in range(max(len(oldPiece),len(newPiece))):
            if i < len(oldPiece):
                if oldPiece[i] in newPiece:
                    continue
                print ("list piece %d is different!" % i)


    return diffList
                
# PURPOSE: recursively the game
def gameCopy(oldGame):
    #find the type we are in
    if type(oldGame) is dict:
        newGame = dict(oldGame)
        for key in newGame.keys():
            if type(key) is dict or type(key) is list:
                newGame[key] = gameCopy(key)

    elif type(oldGame) is list:
        newGame = list(oldGame)
        for thing in newGame:
            if type(key) is dict or type(key) is list:
                newGame[key] = gameCopy(key)
    return newGame

def gameUpdate(old, new):
    if not old:
        old = new
        return
    for key in new[0].keys():
        old[key] = new[0][key]
    for key in new[1].keys():
        toDelete = new[1][key][0]
        toAdd = new[1][key][1]
        #use list comprehension to remake objectlist
        old['objects'][key] = [old['objects'][key][i] for i in range(len(old['objects'][key])) if i not in toDelete]
        old['objects'][key].extend(toAdd) 


if __name__ == "__main__":
    old = copy.deepcopy(sampleGame)
    new = copy.deepcopy(sampleGame)
    new['objects']['starList'][0]['location']['y']=2
    new['state']['turnNumber'] = 1
    diff = gameDiff(old,new)
    gameUpdate(old,diff)
    print (old)

