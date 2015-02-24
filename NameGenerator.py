import math, random, zlib

class LetterLoop:
    letters = list( "abcdefghijklmnopqrstuvwxyz" )
    
    def __init__( self, start = 0 ):
        self.currentNumber = start
        
    def next(self):
        remainder = self.currentNumber
        iteration = 1
        iterationSize = len(self.letters)
        
        while remainder>=iterationSize:
            remainder -= iterationSize
            iterationSize *= len(self.letters)
            iteration  += 1
        result = ''
        
        for i in range( iteration ):
            result = self.letters[remainder % len(self.letters)] + result
            remainder /= len(self.letters)
            
        self.currentNumber += 1
        
        return result
     

class NameGen:
    
    def __init__( self, wordInput = [], accuracy = 15.0 ):
        self.wordInput = wordInput
        self.wordList = {j[0]:int( j[1] ) if j[1] else 1 for j in [[j[0],0] if len( j ) == 1 else j for j in [i.split( "," ) for i in self.wordInput]]}
        self.accuracy = float( accuracy )
    
    #Read file for input formatting
    def readFile( self ):
        with open( self.wordInput ) as f:
            return set( i.replace( "\r\n", "" ) for i in f.readlines() )
  
    
    #Find all invalid combinations of letters
    def invalidCombinations( self, depth = 3 ):
        maxNumber = 0
        for i in xrange( depth ):
            maxNumber += 26**( depth-i )
            
        return set( j for j in set( LetterLoop( i ).next() for i in xrange( maxNumber ) ) if j not in ",".join( self.wordList.keys() ) )
    
    def buildDictionary( self ):
        
        #Iterate through each word to find the letter frequency
        letterGroup = {letter: dict.fromkeys( xrange( int( self.accuracy ) ), 0 ) for letter in LetterLoop.letters}
        letterDetailFrequency = {}
        
        for i in range( int( self.accuracy ) ):
            letterDetailFrequency[i] = {}
            
        for wordToUse in self.wordList.keys():
            wordFrequency = self.wordList[wordToUse]
        
            for letterToUse in LetterLoop.letters:
        
                #Find letter positions
                letterIndex = [i for i, letter in enumerate( wordToUse ) if letter == letterToUse]
                
                #Average over range of 0 to accuracy
                letterAccuracy = self.accuracy/len( wordToUse )
                accuracyIndex = [[i*letterAccuracy,( i+1 )*letterAccuracy] for i in letterIndex]
                
                #Find frequency of letters being used
                for i in accuracyIndex:
                    mainRange = range( int( math.floor( round( i[0], 5 ) ) ), int( math.ceil( round( i[1], 5 ) ) ) )
                    for j in mainRange:
                        startValue = i[0]
                        if j > i[0]:
                            startValue = j
                        endValue = int( startValue )+1
                        if endValue > i[1]:
                            endValue = i[1]
                        letterGroup[letterToUse][int( startValue )] += ( endValue-startValue )*wordFrequency
            
            
            #Calculate frequency of each letter for different points
            for i in range( int( self.accuracy ) ):
                for letter in LetterLoop.letters:
                    letterDetailFrequency[i][letter] = letterGroup[letter][i]
    
    
        #Find average length of words:
        allLengths = [len( word ) for word in self.wordList.keys()]
        uniqueLengths = set( allLengths )
        wordLenths = dict( ( i, allLengths.count( i ) ) for i in uniqueLengths )
    
        return letterDetailFrequency, wordLenths
    
    #Choose a length of a word
    def chooseLength( self, wordLengths ):
        wordLengthRandom = random.randint( 0, sum( wordLengths.values() ) )
        wordLengthCount = 0
        for newWordLength in wordLengths.keys():
            wordLengthCount += wordLengths[newWordLength]
            if wordLengthCount > wordLengthRandom:
                return newWordLength
    
    
    #Figure out which characters to make word from
    def buildWord( self, newWordLength, letterDetailFrequency, invalidCombinations = [], printDebugInfo = 0 ):
        
        newWord = ""
        letterAccuracy = self.accuracy/newWordLength
        totalLoops = 0
        
        maxResets = 10 #Max times the last letter is removed before resetting
        currentResets = 0
        maxRetries = 10 #Max retries to find a new letter
        
        previousInvalidLetter = "~"
        while len( newWord ) < newWordLength:
            i = len( newWord )
            totalLoops += 1
            maxLoops = 50
            if totalLoops > maxLoops:
                if printDebugInfo > 0:
                    print "Hit {0} loops, cancelling generation".format( maxLoops )
                return None
                
            minValue = i*letterAccuracy
            maxValue = (i+1)*letterAccuracy
            minWholeValue = int( math.ceil( round( minValue, 5 ) ) )
            maxWholeValue = int( math.floor( round( maxValue, 5 ) ) )
            
            
            #Calculate what precision bands the letter falls under
            valueRange = xrange( minWholeValue, maxWholeValue )
            individualLetterValues = {i:1 if i in valueRange else 0 for i in xrange( int( self.accuracy ) )}    
            if minValue < minWholeValue:
                individualLetterValues[int( minValue )] = minValue-int( minValue )
            if maxValue > maxWholeValue:
                individualLetterValues[int( maxValue )] = maxValue-int( maxValue )
            
            #Count all letters
            combinedLetterValues = {letter:0 for letter in LetterLoop.letters}
            for i in individualLetterValues.keys():
                for j in combinedLetterValues.keys():
                    combinedLetterValues[j] += letterDetailFrequency[i][j]*i
            
            #Build the word
            currentRetries = 0
            while True:
                
                breakMarker = None
                randomSelection = random.uniform( 0, sum( combinedLetterValues.values() ) )
                i = 0
                
                for letter in combinedLetterValues.keys():
                
                    #Get letter
                    i += combinedLetterValues[letter]
                    
                    if i > randomSelection:
                        
                        if not any( i in newWord+letter for i in invalidCombinations|set([previousInvalidLetter]) ):
                            breakMarker = True
                            newWord += letter
                        break
                
                #Break out of while loop if letter is found
                if breakMarker:
                    break
                 
                #Delete a letter and retry
                if currentRetries and printDebugInfo > 2:
                    print "Invalid last letter, tried to add {0} to {1}".format( letter, newWord )
                    
                if currentRetries > maxRetries:
                    
                    #Fully reset word if maxResets has been hit
                    if currentResets > maxResets:
                        if printDebugInfo > 1:
                            print "Retried building word {0} times, restarting the generation.".format( maxResets )
                        newWord = ""
                        break
                        
                    currentResets += 1
                    currentRetries = -1
                    previousInvalidLetter = newWord[-1:]
                    newWord = newWord[:-1]
                    
                currentRetries += 1
        
        return newWord
    
    @classmethod
    def help( self ):
        print "The format of input must be words in a list, with an optional frequency value given with the word separated by a comma."
        print "    eg. ['Abbey','Abbie','Abby',...] or ['Abbey,100','Abbie,86','Abby,284',...]"
        print "If you have a CSV file, use NameGen( link to file ).readFile() to convert it to a suitable list."
        print
        print "Process the words using NameGen( wordList ).buildDictionary()"
        print "    The first result of the output list [0] is the letter data, and the second [1] is the length data."
        print "Get invalid combinatinons from NameGen( wordList ).invalidCombinations( depth )"
        print "    Depth is the size of combinations to check for and is 3 by default."
        print "Choose a random length based on the input words from NameGen().chooseLength( lengthData )"
        print "Build a word from NameGen().buildWord( length, letterData, invalidCombinations )"


#FIRST NAME
wordData1 = NameGen( "C:/Code/CSV_Database_of_First_Names.csv" ).readFile()    
try:
    rebuiltList = False
    if wordInputHash1 != zlib.crc32( str( wordData1 ) ) or not all( [letterData1, lengthData1] ):
        raise ValueError()
except:
    rebuiltList = True
    wordInputHash1 = zlib.crc32( str( wordData1 ) )
    
    processedWords = NameGen( wordData1 ).buildDictionary()
    letterData1 = processedWords[0]
    lengthData1 = processedWords[1]

invalidCombinationDepth = 3
try:
    if ( lastDepth1 != invalidCombinationDepth or rebuiltList ) or not invalidWords1:
        raise ValueError()
except:
    invalidWords1 = NameGen( wordData1 ).invalidCombinations( invalidCombinationDepth )
    lastDepth1 = invalidCombinationDepth

newWordLength1 = NameGen().chooseLength( lengthData1 )
firstName = NameGen().buildWord( newWordLength1, letterData1, invalidWords1 ).title()

#SECOND NAME

wordData2 = NameGen( "C:/Code/CSV_Database_of_Last_Names.csv" ).readFile()    
try:
    rebuiltList = False
    if wordInputHash2 != zlib.crc32( str( wordData2 ) ) or not all( [letterData2, lengthData2] ):
        raise ValueError()
except:
    rebuiltList = True
    wordInputHash2 = zlib.crc32( str( wordData2 ) )
    
    processedWords = NameGen( wordData2 ).buildDictionary()
    letterData2 = processedWords[0]
    lengthData2 = processedWords[1]

invalidCombinationDepth = 3
try:
    if ( lastDepth2 != invalidCombinationDepth or rebuiltList ) or not invalidWords2:
        raise ValueError()
except:
    invalidWords2 = NameGen( wordData2 ).invalidCombinations( invalidCombinationDepth )
    lastDepth2 = invalidCombinationDepth

newWordLength2 = NameGen().chooseLength( lengthData2 )
lastName = NameGen().buildWord( newWordLength2, letterData2, invalidWords2 ).title()

print firstName, lastName
