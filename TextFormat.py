import random
class TextFormat:
    """
    Format text to replace letters with values. A random value will be chosen if a list has been input.
    
    # Create class object
    >>> animalText = TextFormat( a=["cat, dog"], A=["lizard", "snake", "turtle"] )
    
    # Convert text using the rules
    >>> animalText( "I like /as but I really want my own /A." )
    I like dogs but I really want my own lizard.
    
    # Add a new rule for the current text
    >>> animalText( "I have a /a but I'd quite like a bird, maybe /b." b=["a falcon", "an eagle"] )
    I have a cat but I'd quite like a bird, maybe an eagle.
    
    # Add a new rule permenantly, and replace any existing rules
    >>> animalText.add( b=["a falcon, "an eagle"], a="hamster" )
    animalText( a="hamster", A=["lizard", "snake", "turtle"], b=["a falcon, "an eagle"] )
    
    # Add a new rule permenantly, or add a new item to an existing rule
    >>> animalText.update( b=["a falcon, "an eagle"], a="guinea pig" )
    animalText( a=["hamster", "mouse"], A=["lizard", "snake", "turtle"], b=["a falcon, "an eagle"] )
    
    # Remove a rule
    >>> animalText.remove( 'b', 'A' )
    animalText( a=["hamster", "guinea pig"] )
    
    # Same string with new rules
    >>> animalText( "I like /as but I really want a /A." )
    I like hamsters but I really want a /A.
    
    
    #Other example
    >>> titles_male = ["Mr","Dr","Rev","Lord","Sir","Officer"]
    >>> name_format = TextFormat( t=titles_male )
    >>>
    >>> name_first = "Robert"
    >>> name_middle = "John"
    >>> name_last = "Smith"
    
    >>> name_format("/F /m. /S", F=name_first, f=name_first[:1], M=name_middle, m=name_middle[:1], S=name_last, s=name_last[:1])
    Robert J. Smith
    
    >>> name_format("/t. /f. /S", F=name_first, f=name_first[:1], M=name_middle, m=name_middle[:1], S=name_last, s=name_last[:1])
    Mr R. Smith
    """
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    
    def __repr__(self):
        return "TextFormat('{p}')".format(p=self.kwargs)
        
    def __call__(self, input, **kwargs):
        """Format the input text."""
        
        tempKwargs = self.kwargs
        tempKwargs.update(kwargs)
        
        for replacement in tempKwargs:
            
            if isinstance(tempKwargs[replacement], (list, tuple)):
                newWord = random.choice(tempKwargs[replacement])
            else:
                newWord = tempKwargs[replacement]
            
            input = input.replace('/'+replacement, str(newWord))
        
        return input
    
    
    def update(self, **kwargs):
        """Add new rules or update existing ones."""
        
        for addition in kwargs:
            
            oldValue = self.kwargs.get(addition, None)
            newValue = kwargs[addition]
            
            #Get value already in kwargs
            if not isinstance(oldValue, (list, tuple)):
                if oldValue is not None:
                    oldValue = [oldValue]
                else:
                    oldValue = []
            
            if oldValue != []:
                
                #Update new value
                if not isinstance(newValue, (list, tuple)):
                    newValue = [newValue]
                else:
                    newValue = list(newValue)
                
                #Update original value
                try:
                    self.kwargs[addition] = oldValue+newValue
                except Exception as e:
                    self.kwargs[addition] = oldValue+tuple(newValue)
                
            
    
    def add(self, **kwargs):
        """Add new rules or replace existing ones."""
        self.kwargs.update(kwargs)
    
    def remove(self, *args):
        """Remove rules by letter."""
        for letter in args:
            try:
                del self.kwargs[letter]
            except Exception as e:
                pass
