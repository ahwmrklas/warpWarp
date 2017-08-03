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

    for key in diffKeys:
        diffDict[key] = new[key]

    return diffDict

if __name__ == "__main__":
    old = {'a':1,'b':1}
    new = dict(old)
    new['c'] = 2
    new['a'] = 2
    print(dictDiff(old,new))

