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
    notSetMarker = ':notset:'
    
    def __init__(self, *args, **kwargs):
        self.args = list( args )
        self.kwargs = kwargs
    
    def __repr__(self):
        return self.rawOutput()
    
    def getClassInstance(self):
        """Return class instance."""
        return globals()[self.getClassName()]
    
    def getClassName(self):
        """Return name of class."""
        return self.__class__.__name__
    
    def rawOutput(self):
        """Format the output."""
        
        if self.args and self.kwargs:
            comma = ', '
        else:
            comma = ''
            
        argFormat = ('{}, '*(len(self.args)-1))
        if self.args or self.kwargs:
            argFormat += '{}'
            
        #Return the class object name
        return '{r}({x}{c}{y})'.format(r=self.getClassName(), c=comma,
                                       x=argFormat.format(*self.args),
                                       y=', '.join(k+'='+str(v) for k,v in self.kwargs.iteritems()))
    
    def output(self, args=None, kwargs=None):
        if args is None:
            args = self.args
        if kwargs is None:
            kwargs = self.kwargs
            
        return self.getClassInstance()(*args, **kwargs)
    
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
        return self.output(newArgs, {})
    
    def __len__(self):
        return len(self.args)
    
    """DICTIONARY COMMANDS"""
    def argsToDict(self):
        """Build new dictionary containing args."""
        newDict = self.kwargs.copy()
        newDict.update({None: tuple(self.args)})
        return newDict
        
    def keys(self):
        """Return dictionary keys."""
        return self.kwargs.keys()
        
    def values(self):
        """Return dictionary values."""
        return self.kwargs.values()
        
    def getargs(self):
        """Return args."""
        return self.args
        
    def getkwargs(self):
        """Return kwargs."""
        return self.kwargs
        
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
        
    def get(self, key, optional=notSetMarker):
        """Return a value of a key, or something else if it doesn't exist."""
        if optional != self.notSetMarker:
            return self.kwargs.get(key, optional)
        else:
            return self.kwargs.get(key)
            
    def pop(self, key, optional=notSetMarker):
        """Remove a key, and return something if it fails."""
        if optional != self.notSetMarker:
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
        self.args = {}
        
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
    
    """CONVERSION COMMANDS"""
    def int(self):
        """Try to convert all values to integers."""
        newArgs = tuple(int(float(x)) for x in self.args)
        newKwargs = {i[0]:int(float(i[1])) for i in self.kwargs.iteritems()}
        return self.output(newArgs, newKwargs)
    def __int__(self):
        """Try to convert all values to integers and output the sum."""
        return sum(self.int().allvalues())
        
    def float(self):
        """Try to convert all values to floats."""
        newArgs = tuple(float(x) for x in self.args)
        newKwargs = {i[0]:float(i[1]) for i in self.kwargs.iteritems()}
        return self.output(newArgs, newKwargs)
    def __float__(self):
        """Try to convert all values to floats and output the sum."""
        return sum(self.float().allvalues())
        
    def str(self):
        """Try to convert all values to strings."""
        newArgs = tuple(str(x) for x in self.args)
        newKwargs = {i[0]:str(i[1]) for i in self.kwargs.iteritems()}
        return self.output(newArgs, newKwargs)
    def __str__(self):
        """Try to convert all values to strings and output a formatted string."""
        return self.str().rawOutput()[len(str(self.getClassName()))+1:-1]
    
    def list(self):
        """Return all values as list."""
        return list(self.allValues())
    def tuple(self):
        """Return all values as tuple."""
        return tuple(self.allValues())
    def dict(self):
        return self.argsToDict()
    
    
    """OPERATOR COMMANDS"""
    def joinTwoLists(self, list1, list2, operation, switch=False):
        
        #Get the longest argument list to avoid index problems
        if len(list1) > len(list2):
            argsL = list(list1)
            argsS = list(list2)
        else:
            argsL = list(list2)
            argsS = list(list1)
        
        if switch:
            for i in range(len(argsS)):
                argsL[i] = operation(list2[i], list1[i])
        else:
            for i in range(len(argsS)):
                argsL[i] = operation(list1[i], list2[i])
        
        return argsL
    
    def joinTwoDicts(self, dict1, dict2, operation, switch=False):
        
        #Loop through the dictionary values
        newDict = dict1.copy()
        if switch:
            for i in dict2.keys():
                originalValue = newDict.get(i, None)
                if originalValue is not None:
                    newDict[i] = operation(dict2[i], newDict[i])
                else:
                    newDict[i] = dict2[i]
        else:
            for i in dict2.keys():
                originalValue = newDict.get(i, None)
                if originalValue is not None:
                    newDict[i] = operation(newDict[i], dict2[i])
                else:
                    newDict[i] = dict2[i]
        return newDict
                
    def op(self, other, operation, switch=False):
        
        #If it is a NewTuple value
        if isinstance( other, self.getClassInstance() ):
            newKwargs = self.joinTwoDicts(self.kwargs, other, operation, switch)
            newArgs = self.joinTwoLists(self.args, other.getargs(), operation, switch)
            
        #If it is a list or tuple
        elif isinstance(other, (tuple, list)):
            newArgs = self.joinTwoLists(self.args, other, operation, switch)
            newKwargs = self.kwargs
        
        #If it is a dictionary
        elif isinstance(other, dict):
            newArgs = self.args
            newKwargs = self.joinTwoDicts(self.kwargs, other, operation, switch)
            
        #If it is something like a letter or number
        else:
            newArgs = self.args
            newKwargs = self.kwargs.copy()
            
            if switch:
                for i in range(len(newArgs)):
                    newArgs[i] = operation(newArgs[i], other)
                for key in newKwargs:
                    newKwargs[key] = operation(newKwargs[key], other)
            else:
                for i in range(len(newArgs)):
                    newArgs[i] = operation(newArgs[i], other)
                for key in newKwargs:
                    newKwargs[key] = operation(newKwargs[key], other)
        
        return self.output(newArgs, newKwargs)
    
    #Addition
    def opAdd(self, a, b):
        return a+b
    def __add__(self, other):
        return self.op(other, self.opAdd)
    def __radd__(self, other):
        return self.op(other, self.opAdd, True)
    
    #Subtraction
    def opSub(self, a, b):
        return a-b
    def __sub__(self, other):
        return self.op(other, self.opSub)
    def __rsub__(self, other):
        return self.op(other, self.opSub, True)
        
    #Multiplication
    def opMul(self, a, b):
        return a*b
    def __mul__(self, other):
        return self.op(other, self.opMul)
    def __rmul__(self, other):
        return self.op(other, self.opMul, True)
        
    #Divison
    def opDiv(self, a, b):
        return a/b
    def __div__(self, other):
        return self.op(other, self.opDiv)
    def __rdiv__(self, other):
        return self.op(other, self.opDiv, True)
        
    #Exponent
    def opPow(self, a, b):
        return a**b
    def __pow__(self, other):
        return self.op(other, self.opPow)
    def __rpow__(self, other):
        return self.op(other, self.opPow, True)

    #Modulo
    def opMod(self, a, b):
        return a%b
    def __mod__(self, other):
        return self.op(other, self.opMod)
    def __rmod__(self, other):
        return self.op(other, self.opMod, True)
        
    #Absolute value (always positive)
    def __abs__(self):
        newArgs = self.args
        newKwargs = self.kwargs.copy()
        newArgs = [abs(i) for i in newArgs]
        newKwargs = {i[0]:abs(i[1]) for i in newKwargs.iteritems()}
        return self.output(newArgs, newKwargs)
