key = "hidden"
input = "test"

import zlib, random, cPickle, base64

#Set the random seed
keyLength = len( key )
keyCRC = zlib.crc32( key )
splitKey = list( key )
random.seed( keyCRC )

#Generate new key from the random seed
newKey = ""
newKeyLength = 12
i = 0
while len( newKey ) < newKeyLength:
    newKey += random.choice( str( abs( zlib.crc32( key[i%len( key )] ) ) ) )
    i += 1
newKeyList = [( int( x )*random.randint( 0, 255 ) )%255 for x in list( newKey )]
random.shuffle( newKeyList )

#Decide how many extra characters to add for each character
extraCharacters = [random.randint( 0, max( 1, int( keyLength**0.5 ) ) ) for x in xrange( keyLength+1 )]
charactersToAdd = [random.randint( 0, 255 ) for x in xrange( sum( extraCharacters ) + len( extraCharacters ) )]

#Encode the characters using the key
encodedString = ""
increment = 0
for i in range( len( input ) ):
    letterToChange = input[i]
    characterNumber = ord( letterToChange )
    for j in xrange( extraCharacters[i%len( extraCharacters )]+1 ):
        encodedString += chr( ( characterNumber+newKeyList[increment%len( newKeyList )]+charactersToAdd[increment%len( charactersToAdd )] ) % 255 )
        increment += 1
encodedString = base64.b64encode( encodedString )

print encodedString

#Decode the characters using the key
input = encodedString
try:
    encodedString = base64.b64decode( input )
except:
    print "Invalid input"
extraCharactersIncrement = [extraCharacters[0]]
increment = 0
while extraCharactersIncrement[-1] < len( encodedString ):
    increment += 1
    extraCharactersIncrement.append( extraCharactersIncrement[-1]+extraCharacters[increment%len( extraCharacters )]+1 )
extraCharactersIncrement = extraCharactersIncrement[:-1]
charactersToRemove = [charactersToAdd[i%len( charactersToAdd )]+newKeyList[i%len( newKeyList )] for i in extraCharactersIncrement]
decodedString = ""
for i in extraCharactersIncrement:
    decodedString += chr( ( ord( encodedString[i] )-newKeyList[i%len( newKeyList )]-charactersToAdd[i%len( charactersToAdd )] )%255 )

print decodedString
