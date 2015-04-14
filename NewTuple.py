class NewTuple:
    """
    value = NewTuple(3, 5, x=2)
    
    >>> value + 10
    NewTuple(13, 15, x=12)
    
    >>> value + [10]
    NewTuple(3, 5, 10, x=2)
    
    >>> value + {x:5}
    NewTuple(3, 5, x=7)
    
    >>> value + {j:5}
    NewTuple(3, 5, x=2, j=5)
    
    >>> value + NewTuple(2)
    NewTuple(5, 5, x=2)
    
    >>> value + NewTuple(j=5)
    NewTuple(2, 5, x=2, j=5)
    """
    
    def __init__(self, *args, **kwargs):
        self.args = list( args )
        self.kwargs = kwargs
    
    def __repr__(self):
        """Build class object."""
        return self.rawOutput()
    
    def getClassName(self):
        """Return name of class."""
        return globals()[self.__class__.__name__]
    
    def rawOutput(self):
        """Format the output."""
        
        argFormat = ('{}, '*(len(self.args)-1))
        if self.args and self.kwargs:
            comma = ', '
            argFormat += '{}'
        else:
            comma = ''
            
        #Return the class object name
        return '{r}({x}{c}{y})'.format(r=self.getClassName(), c=comma,
                                       x=argFormat.format(*self.args),
                                       y=', '.join(k+'='+str(v) for k,v in self.kwargs.iteritems()))
    
    def output(self, args=None, kwargs=None):
        if args is None:
            args = self.args
        if kwargs is None:
            kwargs = self.kwargs
        print kwargs
        return self.getClassName()(*args, **kwargs)
    
    #Get indexes
    def __getitem__(self, item):
        """
        Get specificed index at a[b], a['b':'c'], or a[b:c:d].
        a[b:c] goes to __getslice__ instead, if b and c are integers.
        
        b = start
        c = stop
        d = step
        """
        if not isinstance( item, slice ):
            try:
                #Return dictionary value
                return self.kwargs[item]
            except KeyError:
                try:
                    #Return index value
                    return self.args[int(item)]
                #Can be TypeError or ValueError if int() fails
                except Exception as e:
                    if isinstance(item, (str, unicode)):
                        #Key doesn't exist
                        raise KeyError("item '{}' not found in dictionary".format(item))
                    else:
                        #List index out of range
                        raise TypeError(e.message)
        else:
            #Find which values are provided
            try:
                start = int(item.start)
            except:
                start = 0
            try:
                stop = int(item.stop)
            except:
                stop = len(self.args)
            try:
                step = int(item.step)
            except:
                step = 1
            #Use inbuilt python slicing
            return tuple( self.args )[start:stop:step]
                   
    def __getslice__(self, start, stop):
        """
        Get specificed index at a[b:c]
        
        b = start
        c = stop
        """
        newArgs = self.values()[start:stop]
        newKwargs = {}
        return self.output(newArgs, {})
    
    def __len__(self):
        return len(self.args)
    
    """Dictionary commands"""
    def argsToDict(self):
        """Build new dictionary containing args."""
        newDict = self.kwargs.copy()
        newDict.update({None: tuple(self.args)})
        return newDict
    def keys(self):
        """Return dictionary keys."""
        return self.kwargs.keys()
    def values(self):
        """Return non dictionary values."""
        return self.args
    def allvalues(self):
        """Return both dictionary and non dictionary values."""
        return self.values() + self.kwargs.values()
    def items(self):
        """Return all items as a dictionary."""
        newDict = self.argsToDict()
        return newDict.items()
    def iteritems(self):
        """Iterator through dictionary (keys, values)."""
        return self.kwargs.iteritems()
    def iterkeys(self):
        """Iterator through dictionary keys."""
        return self.kwargs.iterkeys()
    def itervalues(self):
        """Iterator through dictionary values."""
        return self.kwargs.itervalues()
    def has_key(self, key):
        """If the dictionary contains a key."""
        return self.kwargs.has_key(key)
    def pop(self, key, optional=None):
        """Remove a key, and return something if it fails."""
        if optional:
            return self.kwargs.pop(key, optional)
        else:
            return self.kwargs.pop(key)
            
    def clear(self):
        """Clear all values."""
        self.kwargs = {}
        self.args = {}
    def cleardict(self):
        """Only clear dictionary values."""
        self.kwargs = {}
    def clearvalues(self):
        """Only clear non dictionary values."""
        
    def __delitem__(self, key):
        """Delete a dictionary key - (del a[b])"""
        try:
            del self.kwargs[key]
        except:
            try:
                key = int(key)
                self.args[key]
                self.args = self.args[:key]+self.args[key+1:]
            except TypeError, ValueError:
                raise KeyError("key '{}' not found in dictionary".format(key))
        
    def __setitem__(self, key, value):
        """Add a dictionary key - a[b]=c"""
        self.kwargs[key] = value
        print self.kwargs
        print self.args
    
    def int(self):
        """Try to convert all values to integers."""
        self.args = tuple(int(float(x)) for x in self.args)
        self.kwargs = {i[0]:int(float(i[1])) for i in self.kwargs.iteritems()}
        return self.output()
    def __int__(self):
        """Try to convert all values to integers and output the sum."""
        return sum(self.int().allvalues())
        
    def float(self):
        """Try to convert all values to floats."""
        self.args = tuple(float(x) for x in self.args)
        self.kwargs = {i[0]:float(i[1]) for i in self.kwargs.iteritems()}
        return self.output()
    def __float__(self):
        """Try to convert all values to floats and output the sum."""
        return sum(self.float().allvalues())
        
    def str(self):
        """Try to convert all values to strings."""
        self.args = tuple(str(x) for x in self.args)
        self.kwargs = {i[0]:str(i[1]) for i in self.kwargs.iteritems()}
        return self.output()
    def __str__(self):
        """Try to convert all values to strings and output a formatted string."""
        return self.str().rawOutput()[len(str(self.getClassName()))+1:-1]
    
    def list(self):
        """Return all values as list."""
        return list(self.allValues())
    def tuple(self):
        """Return all values as tuple."""
        return tuple(self.allValues())
