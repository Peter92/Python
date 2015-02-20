import md5, random, cPickle, base64, zlib

class Encrypt:
    
    def __init__( self, key, keyLength = 128 ):
        
        #Set the random seed
        m = md5.new()
        m.update( key )
        random.seed( m.digest() )
        
        #Generate new key from the random seed
        newKey = ""
        newKeyLength = keyLength
        i = 0
        while len( newKey ) < newKeyLength:
            newKey += random.choice( str( abs( zlib.crc32( key[i%len( key )] ) ) ) )
            i += 1
        self.newKeyList = [( int( x )*random.randint( 0, 255 ) )%255 for x in list( newKey )]
        self.newKeyListLength = len( self.newKeyList )
        random.shuffle( self.newKeyList )
        
        #Decide how many extra characters to add for each character
        originalKeyLength = len( key )
        self.extraCharacters = [random.randint( 0, max( 1, int( originalKeyLength**0.5 ) ) ) for x in xrange( originalKeyLength+1 )]
        self.charactersToAdd = [random.randint( 0, 255 ) for x in xrange( sum( self.extraCharacters ) + len( self.extraCharacters ) )]
        self.extraCharactersLength = len( self.extraCharacters )
        self.charactersToAddLength = len( self.charactersToAdd )
        
    def encode( self, input ):
        
        #Change letters based on values calculated from the key
        i = 0
        encodedString = ""
        for j in range( len( input ) ):
            
            letterToChange = input[j]
            characterNumber = ord( letterToChange )
            
            #Add extra letters so the word size is not so obvious
            for k in xrange( self.extraCharacters[j%self.extraCharactersLength]+1 ):
                encodedString += chr( ( characterNumber+self.newKeyList[i%self.newKeyListLength]+self.charactersToAdd[i%self.charactersToAddLength] )%255 )
                i += 1
        
        return base64.b64encode( encodedString )
        
    def decode( self, input ):
        
        #Check string is in base64
        try:
            encodedString = base64.b64decode( input )
        except:
            print "Invalid input"
            return None
            
        #Find the indexes where the original letters should be
        extraCharactersIncrement = [self.extraCharacters[0]]
        i = 0
        while extraCharactersIncrement[-1] < len( encodedString ):
            i += 1
            extraCharactersIncrement.append( extraCharactersIncrement[-1]+self.extraCharacters[i%self.extraCharactersLength]+1 )
        extraCharactersIncrement = extraCharactersIncrement[:-1]
        
        #Decode the string
        decodedString = "".join( chr( ( ord( encodedString[i] )-self.newKeyList[i%self.newKeyListLength]-self.charactersToAdd[i%self.charactersToAddLength] )%255 ) for i in extraCharactersIncrement )

        return decodedString
