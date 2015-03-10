class EditError( Exception ):
    pass
def editDictionary( dictionaryName, listOfValues, canOverwriteKeys=True ):
    reducedDictionary = dictionaryName
    for i in listOfValues[:-2]:
        if type( reducedDictionary ) != dict and canOverwriteKeys:
            reducedDictionary = {}
        try:
            if reducedDictionary.get( i, None ) == None:
                canOverwriteKeys = True
                raise EditError()
            elif type( reducedDictionary[i] ) != dict:
                raise EditError()
        except EditError:
            reducedDictionary[i] = {}
        except:
            print "Something went wrong"
            return
        reducedDictionary = reducedDictionary[i]
    if canOverwriteKeys or ( not canOverwriteKeys and not reducedDictionary.get( listOfValues[-2], None ) ):
        reducedDictionary[listOfValues[-2]] = listOfValues[-1]
        return True
    else:
        return False
