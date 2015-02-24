import math, random, zlib
global letterGroup
global accuracy
accuracy = 15.0

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
        
'''
with open("C:/Code/words.csv") as f:
    wordInput = set( word.replace("\r\n", "") for word in f.readlines() )

    wordList = [[str( splitWord[0] ), int( splitWord[1] )] if len( splitWord )>1 and splitWord[1].isdigit() else [str( splitWord[0] ), 1] for splitWord in wordInput]
'''

with open("C:/Code/wordsEn.txt") as f:
    wordInput = set( i.replace( "\r\n", "" ) for i in f.readlines() )

#Build list into a dictionary
try:
    if wordInputHash != zlib.crc32( str( wordInput ) ):
        raise ValueError()
except:
    wordList = {j[0]:int( j[1] ) if j[1] else 1 for j in [[j[0],0] if len( j ) == 1 else j for j in [i.split( "," ) for i in wordInput]]}
    wordInputHash = zlib.crc32( str( wordInput ) )

#Find range from a to z*(maxDepth)
maxDepth = 3
maxNumber = 0
for i in xrange( maxDepth ):
    maxNumber += 26**( maxDepth-i )

#Calculate any combinates that don't exist in input word list
try:
    if lastMaxDepth != maxDepth:
        raise ValueError()
except:
    allWordsJoined = ",".join( allWords )
    invalidCombinations = set( j for j in set( LetterLoop( i ).next() for i in xrange( maxNumber ) ) if j not in allWordsJoined )
    lastMaxDepth = maxDepth

    #Iterate through each word to find the letter frequency
    letterGroup = {letter: dict.fromkeys( xrange( int( accuracy ) ), 0 ) for letter in LetterLoop.letters}
    letterDetailFrequency = {}
    
    for i in range( int( accuracy ) ):
        letterDetailFrequency[i] = {}
        
    for wordToUse in wordList.keys():
        wordFrequency = wordList[wordToUse]
    
        for letterToUse in LetterLoop.letters:
    
            #Find letter positions
            letterIndex = [i for i, letter in enumerate( wordToUse ) if letter == letterToUse]
            
            #Average over range of 0 to accuracy
            letterAccuracy = accuracy/len( wordToUse )
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
        for i in range( int( accuracy ) ):
            for letter in LetterLoop.letters:
                letterDetailFrequency[i][letter] = letterGroup[letter][i]


    #Find average length of words:
    allLengths = [len( word ) for word in allWords]
    uniqueLengths = set( allLengths )
    wordLenths = dict( ( i, allLengths.count( i ) ) for i in uniqueLengths )



#Choose a length of a word
wordLengthRandom = random.randint( 0, sum( wordLenths.values() ) )
wordLengthCount = 0
for newWordLength in wordLenths.keys():
    wordLengthCount += wordLenths[newWordLength]
    if wordLengthCount > wordLengthRandom:
        break
newWord = ""

maxMultiple = accuracy/newWordLength
totalLetters = 0

#Figure out which characters to make word from
letterAccuracy = accuracy/newWordLength
for i in range( newWordLength ):
    minValue = i*letterAccuracy
    maxValue = (i+1)*letterAccuracy
    minWholeValue = int( math.ceil( round( minValue, 5 ) ) )
    maxWholeValue = int( math.floor( round( maxValue, 5 ) ) )
    
    
    #Calculate what precision bands the letter falls under
    valueRange = xrange( minWholeValue, maxWholeValue )
    individualLetterValues = {i:1 if i in valueRange else 0 for i in xrange( int( accuracy ) )}    
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
    maxRetries = 10
    currentRetries = 0
    
    
    
    while True:
        
        breakMarker = None
        randomSelection = random.uniform( 0, sum( combinedLetterValues.values() ) )
        i = 0
        
        for letter in combinedLetterValues.keys():
        
            #Get letter
            i += combinedLetterValues[letter]
            
            if i > randomSelection:
                
                if not any( i in newWord+letter for i in invalidCombinations ):
                    breakMarker = True
                    newWord += letter
                    break
                    
        if breakMarker or currentRetries > maxRetries:
            if currentRetries > maxRetries:
                print 351513
            break
        currentRetries += 1
                    

print newWord.title()
            
