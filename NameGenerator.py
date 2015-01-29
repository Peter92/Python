import math, random
global letterGroup
global wordSize
global detail
detail = 15.0
letterGroup = {}
try:
    letterGroup["a"][0]
except:
    letterGroup = {}
try:
    wordSize
except:
    wordSize = {}
    
class LetterLoop:
    def __init__( self, start = 0 ):
        self.letters = list( "abcdefghijklmnopqrstuvwxyz" )
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

def addLetters( wordToUse, letterToUse, wordFrequency ):

    letterIndex = [i for i, letter in enumerate( wordToUse ) if letter == letterToUse]
    
    wordLength = len( wordToUse )
    
    letterDetail = detail/wordLength
    detailIndex = [[i*letterDetail,( i+1 )*letterDetail] for i in letterIndex]
    
    for i in detailIndex:
        mainRange = range( int( math.floor( round( i[0], 5 ) ) ), int( math.ceil( round( i[1], 5 ) ) ) )
        for j in mainRange:
            startValue = i[0]
            if j > i[0]:
                startValue = j
            endValue = int( startValue )+1
            if endValue > i[1]:
                endValue = i[1]
            
            letterGroup[letterToUse][int( startValue )] += ( endValue-startValue )*wordFrequency
            
            
def iterateWords( wordList ):
    
    for letter in list( "abcdefghijklmnopqrstuvwxyz" ):
        
        try:
            letterGroup[letter]
        except:
            letterGroup[letter] = {}
            
        for i in range( int( detail ) ):
            try:
                letterGroup[letter][i]
            except:
                letterGroup[letter][i] = 0
        
        for words in wordList:
            
            wordLength = len( words[0] )
            try:
                wordSize[wordLength] += 1
            except:
                wordSize[wordLength] = 1
            
            addLetters( words[0], letter, words[1] )
    
    letterDetailFrequency = {}
    for i in range( int( detail ) ):
        letterDetailFrequency[i] = {}
        for letter in list( "abcdefghijklmnopqrstuvwxyz" ):
            letterDetailFrequency[i][letter] = letterGroup[letter][i]
    
    return letterDetailFrequency
    

def createNewWord( letterDetailFrequency, invalidRules = [], minWordSize = 0, maxWordSize = 100, newWordLength = -1 ):

    newWord = []
    
    while not minWordSize <= newWordLength <= maxWordSize:
        wordSizeSum = sum( frequency for size, frequency in wordSize.iteritems() )
        randomNumber = random.uniform( 0, wordSizeSum )
        frequencyCount = 0
        for size in wordSize:
            frequencyCount += wordSize[size]
            if frequencyCount > randomNumber:
                newWordLength = size
                break
            
    maxMultiple = detail/newWordLength
        
    i = 0
    while i < newWordLength:
        
        letterPosition = int( round( i*maxMultiple + maxMultiple/2.0 ) )
        allLetters = letterDetailFrequency[ letterPosition ]
        allLettersSum = sum( frequency for letter, frequency in allLetters.iteritems() )
        
        randomNumber = random.uniform( 0, allLettersSum )
        frequencyCount = 0
        for letter in allLetters:
            frequencyCount += allLetters[letter]
            if frequencyCount > randomNumber:
                #Make sure 3 letters don't follow each other
                if i > 2:
                    if newWord[-1].lower() == letter and newWord[-2].lower() == letter:
                        break
                newWord.append( letter )
                i += 1
                break
    
    newWord = "".join( newWord )
    if any( vowel in newWord for vowel in ["a","e","i","o","u"] ):
        if not any( i in newWord for i in invalidRules ):
            return newWord.title()
    try:
        return createNewWord( letterDetailFrequency, invalidRules, minWordSize, maxWordSize, len( newWord ) )
    except:
        pass


def getInvalidCombinations( allWords, maxDepth = 3 ):
    
    
    allLetters = list( "abcdefghijklmnopqrstuvwxyz" )
    invalidCombinations = []
    
    maxNumber = 0
    for i in range( maxDepth ):
        maxNumber += 26**( maxDepth-i )
            
    for i in range( maxNumber ):
        letterCombination = LetterLoop(i).next()
        if letterCombination not in allWords:
            invalidCombinations.append( letterCombination )
    
    return invalidCombinations

#Need a file with lines set up as: word, frequency
with open("C:/Code/words.csv") as f:
    content = [i.replace("\r\n", "").split( "," ) for i in f.readlines()]
    content = [[str( i[0] ), int( i[1] )] for i in content if i[1].isdigit()]
letterDetailFrequency = iterateWords( content )

#Need a file with lines set up as: word
with open("C:/Code/wordsEn.txt") as f:
    allWords = ",".join( [i.replace( "\r\n", "" ) for i in f.readlines()] )


try:
    invalidCombinations
except:
    maxDepth = 5
    invalidCombinations = getInvalidCombinations( allWords, maxDepth )

for i in range( 30 ):
    '''
    newWord = createNewWord( letterDetailFrequency, invalidCombinations, 3, random.randint( 7, 10 ) )
    if newWord:
        print newWord
    '''
    firstName = createNewWord( letterDetailFrequency, invalidCombinations, 3, random.randint( 5, 8 ) )
    surname = createNewWord( letterDetailFrequency, invalidCombinations, 4, random.randint( 8, 12 ) )
    if firstName and surname:
        print "{0} {1}".format( firstName, surname )
