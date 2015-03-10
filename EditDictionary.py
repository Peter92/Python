def editDictionary( dictionaryName, listOfValues, canOverwriteKeys=True ):
    reducedDictionary = dictionaryName
    for i in valueList[:-2]:
        if type( reducedDictionary ) != dict:
            reducedDictionary = {}
        try:
            if reducedDictionary.get( i, False ) == False:
                raise ValueError()
            elif type( reducedDictionary[i] ) != dict:
                if not canOverwriteKeys:
                    return
                raise KeyError()
        except( ValueError, KeyError ):
            reducedDictionary[i] = {}
        except:
            print "Something went wrong"
            return
        reducedDictionary = reducedDictionary[i]
    reducedDictionary[valueList[-2]] = valueList[-1]
