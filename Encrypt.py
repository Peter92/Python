key = "hidden"
input = "test"

import zlib
import random
keyLength = len( key )
keyCRC = zlib.crc32( key )
random.seed( crc )
splitKey = list( key )


#Generate new key from the random seed
newKey = ""
newKeyLength = 128
i = 0
while len( newKey ) < newKeyLength:
    if i+2 > keyLength:
        i = 0
    i += 1
    newKey += random.choice( str( abs( zlib.crc32( key[i] ) ) ) )
    
newKeyList = [( int( x )*random.randint( 0, 255 ) )%255 for x in list( newKey )]
random.shuffle( newKeyList )

#Change the characters using the key
encodedString = ""
for i in range( len( input ) ):
    letterToChange = input[i]
    characterNumber = ord( letterToChange )
    encodedString += chr( ( characterNumber + newKeyList[i] ) % 255 )
    

#Unchange the characters using the key
decodedString = ""
for i in range( len( input ) ):
    encodedCharacter = ord( encodedString[i] )
    keyCharacter = ord( input[i] )
    if encodedCharacter < keyCharacter+newKeyList[i]:
        encodedCharacter += 255
        
    decodedString += chr( encodedCharacter-newKeyList[i] )
    
print encodedString
print decodedString
