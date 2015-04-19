from decimal import Decimal, getcontext
from random import shuffle, seed

#number = "675031636802469384872148105925333571413414219059059077491522580707629077866018102360401609886075741917049577624505725884425285578623843322305362201#10:86"
number = "25f3.4"
currentBase = 16
newBase = 10
decimalPoints = True
decimalPrecision = 50

#Extra input
outputBaseUsed = False

#Set up sequence order
sequenceNumber = "0123456789"
sequenceLetter = "abcdefghijklmnopqrstuvwxyz"
sequenceSymbols = "= _%/^~,:;?!+-<>{}()[]|."
sequence = list( sequenceNumber ) + list( sequenceLetter ) + list( sequenceLetter.upper() ) + list( sequenceSymbols )

#Set up precision
if decimalPrecision < 8:
    decimalPrecision = 8
getcontext().prec = decimalPrecision

#Format number
number = str( number )
if number[0] == "-":
    output = "-"
    number = number[1:]

#Copy base from input number
if "#" in str( number ):
    numberInfo = str( number ).split( "#" )[1].split( ":" )
    currentBase = int( numberInfo[0] )
    newBase = int( numberInfo[1] )
    number = str( number ).split( "#" )[0]
    #outputBaseUsed = False
if currentBase > 1 and newBase > 1:
    valid = True
else:
    valid = False
    print "Invalid base number."
output = ""
#if outputBaseUsed == True:
#    decimalPoints = False

#Split decimal numbers
if "." in number and decimalPoints == True:
    numberSplit = number.split( "." )
    if len( numberSplit ) > 2:
        valid = False
        print "Too many decimal points."
else:
    numberSplit = [number, "0"]
numberInteger = numberSplit[0]
numberDecimal = numberSplit[1]


if currentBase > len( sequence ) or newBase > len( sequence ):
    valid = False
    print "Base number too high, maximum is " + str( len( sequence ) )

if valid == True:
    #Convert numbers to base 10
    convertedIntegers = {}
    decimalNumber = {}
    for j in range( 2 ):
        decimalNumber[j] = 0
        originalNumberList = list( numberSplit[j] )
        convertedIntegers[j] = []
        for i in range( len( originalNumberList ) ):
            originalValue = originalNumberList[i]
            try:
                convertedIntegers[j].append( [index for index, x in enumerate( sequence[0:currentBase] ) if x == originalValue][0] )
            except:
                valid = False
                print "Invalid input number."
                break
            if j == 0:
                decimalNumber[j] += convertedIntegers[j][-1]*currentBase**( len( originalNumberList )-i-1 )
            if j == 1:
                decimalNumber[j] += Decimal( convertedIntegers[j][-1] )/Decimal( currentBase**( i+1.0 ) )

if valid == True:
    #Calculate how many integers the final number should have
    decimalRemainder = decimalNumber[0]
    multiples = 0
    while decimalRemainder >= newBase:
        decimalRemainder /= newBase
        multiples += 1
   
    #Convert to integer values of new base
    outputNumbers = []
    for i in range( multiples + 1 ):
        outputNumbers.append( decimalNumber[0] / newBase ** ( multiples-i ) )
        decimalNumber[0] -= outputNumbers[-1] * newBase ** ( multiples-i )
   
    #Calculate decimals
    decimalInteger = []
    decimalRemainder = decimalNumber[1]
    truncated = False
    while decimalRemainder != 0:
        multipliedDecimal = decimalRemainder*newBase
        convertedDecimal = str( multipliedDecimal ).split( "." )
        decimalInteger.append( int( convertedDecimal[0] ) )
        decimalRemainder = Decimal( "0."+convertedDecimal[1] )
        if len( decimalInteger ) == decimalPrecision:
            truncated = True
            break
   
    #Convert to letters
    for i in range( len( outputNumbers ) ):
        output += sequence[outputNumbers[i]]
    if len( decimalInteger ) > 0:
        output += "."
        for i in range( len( decimalInteger ) ):
            output += sequence[decimalInteger[i]]
    if truncated == True:
        output += "..."
    if outputBaseUsed == True:
        output += "#" + str( newBase ) + ":" + str( currentBase )

    print output
