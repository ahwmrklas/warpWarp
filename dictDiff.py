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
        else:
            #this gets tricky. if its a dictionary, recurse.
            if type(new[key]) is dict:
                if dictDiff(old[key],new[key]):
                    diffDict[key] = new[key]

    for key in diffKeys:
        diffDict[key] = new[key]

    return diffDict

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


if __name__ == "__main__":
    base = {'a':1,'b':1}
    old = dict(base)
    old['c'] = [1,2,3]
    new = {'a':1, 'b':1, 'c':[1,2,3]}
    new['d'] = 2
    new['a'] = 2
    new['c'][1] = 7
    print(old)
    print(new)
    print(dictDiff(old,new))

