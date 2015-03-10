dictionaryValue = {"data": dict.fromkeys( [0, 1, 2, 3] ), "data2": {0: "test",1:"test2"}}

reducedDictionary = dictionaryValue
valueList = ["data", 1, 64, "Testing", "value"]
canOverwriteKeys = True
for i in valueList[:-2]:
    exceptionOccured = False
    try:
        if type( reducedDictionary ) != dict:
            raise ValueError()
        elif reducedDictionary.get( i, False ) == False:
            raise KeyError()
    except ValueError:
        print "not dictionary"
        reducedDictionary = {}
        exceptionOccured = True
    except KeyError:
        print "key doesn't exist"
        exceptionOccured = True
    if exceptionOccured or ( type( reducedDictionary[i] ) != dict and canOverwriteKeys ):
        print "setting key value"
        reducedDictionary[i] = {}
    reducedDictionary = reducedDictionary[i]
reducedDictionary[valueList[-2]] = valueList[-1]
print dictionaryValue
