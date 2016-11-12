from __future__ import division
split = str.split

def power_of_10(value, exp):
    """Raise any value to a power of 10 without floating point issues.
    It works by editing the string itself.
    """
    number = LargeNumber(value)
    num, decimal = map(list, (number.integer, number.decimal))
    if num[0] == '-':
        negative = True
        del num[0]
    else:
        negative = False
    while exp > 0:
        exp -= 1
        try:
            next_val = decimal.pop(0)
        except IndexError:
            next_val = '0'
        num.append(next_val)
    while exp < 0:
        exp += 1
        try:
            next_val = num.pop()
        except IndexError:
            next_val = '0'
        decimal.insert(0, next_val)
    if num:
        result = str(int(''.join(num)))
    else:
        result = '0'
    stripped_decimal = ''.join(decimal).rstrip('0')
    if stripped_decimal:
        result += '.' + stripped_decimal
    else:
        result += '.0'
    if negative:
        result = '-' + result
    return LargeNumber(result)
    
    
class LargeNumber(object):
    """Display and perform basic calculations on numbers of any size, without losing any precision.
    
    Tests:
        Addition:
        >>> LargeNumber(5) + 10
        LargeNumber('15.0')
        
        Subtraction:
        >>> LargeNumber(5) - 10.1252
        LargeNumber('-5.1252')
        
        Multiplication:
        >>> LargeNumber(5) * 10
        LargeNumber('50.0')
        
        Division:
        >>> LargeNumber(5232.91875) / 2.55
        LargeNumber('2052.125')
        >>> LargeNumber(-5232.91875) // 2.55
        LargeNumber('-2053.0')
        
        Modulus:
        >>> LargeNumber('26.32') % 2
        LargeNumber('0.32')
        >>> LargeNumber('26.32') % -2.703
        LargeNumber('-0.71')
        
        Powers:
        >>> LargeNumber('26.32') ** 5
        LargeNumber('12630758.3021842432')
        >>> LargeNumber('26.32', precision=12) ** -2
        LargeNumber('0.0014435380308755')
        
        Using huge numbers:
        >>> (LargeNumber('1' + '0' * 100) ** -2).format()
        '1.0e-200'
        >>> (LargeNumber('1' + '23' * 1053 + '.725') * ('6' + '705' * 350)).format()
        '8.26359693027e+3156'
    """
    
    def __init__(self, number, precision=100):
        """Split the number into two parts and detect if negative."""
        self.number = str(number)
        
        #Find if negative
        if self.number[0] == '-':
            self.negative = True
            self.number = self.number[1:]
        else:
            self.negative = False
        
        #Split decimal
        if '.' in self.number:
            try:
                self.integer, self.decimal = self.number.split('.')
                map(int, (self.integer, self.decimal))
            except ValueError:
                raise TypeError('invalid number: {}'.format(self.number))
        else:
            self.integer, self.decimal = self.number, '0'
        
        self.exact = True
        self.precision = precision
        self.refresh()
        
        
    def refresh(self):
        """Set variables that may need to be recalculated later."""
        
        #Set to positive if its -0.0
        if not self.integer and not self.decimal:
            self.negative = False
        self.multiplier = -1 if self.negative else 1
            
        self.integer = str(int(self.integer))
    
    
    def __str__(self):
        """Return the number as a string."""
        value = self.integer + '.' + self.decimal
        if self.negative:
            value = '-' + value
        return value
    
    
    def __repr__(self):
        return 'LargeNumber(\'{n}{i}.{d}\')'.format(n = '-' if self.negative else '', i=self.integer, d=self.decimal)
    
    
    def __eq__(self, new):
        """Return if current number is equal to another number.
        
        Tests:
            >>> LargeNumber(3) == 3
            True
            >>> LargeNumber(-3) == 3
            False
            >>> LargeNumber(-0.1) == 0.1
            False
            >>> LargeNumber('5000.3516105') == '5000.3516105'
            True
            >>> LargeNumber(2) * LargeNumber(0.9531) == 2 * 0.9531
            True
            >>> LargeNumber(2.02988853) * LargeNumber(0.9531) == '1.934686757943'
            True
            >>> LargeNumber(2.02988853) * LargeNumber(0.9531) == LargeNumber(2.02988853) * LargeNumber(0.95312)
            False
        """
        if not isinstance(new, LargeNumber):
            try:
                new = LargeNumber(new)
            except TypeError:
                return False
        
        return self.integer * self.multiplier == new.integer and self.decimal == new.decimal
        
    
    def _compare(self, new):
        """Compare two numbers and return a value.
        
        Tests:
            >>> LargeNumber(5)._compare(7)
            2
            >>> LargeNumber(5)._compare(-7)
            1
            >>> LargeNumber('-5.7882453351')._compare('-5.7882453351')
            3
            >>> LargeNumber('-5.7882453351')._compare('-5.7882453352')
            1
            >>> LargeNumber('-5.7882453351')._compare('-5.788245335')
            2
            >>> LargeNumber('2' * 1000)._compare('2' * 1000 + '.0001')
            2
        """
        used_decimal = False
        greater_than = 1
        less_than = 2
        equals = 3
        
        if not isinstance(new, LargeNumber):
            new = LargeNumber(new)
            
        #Choose whether to use integers or decimals to compare
        if self.integer != new.integer:
            comp1, comp2 = map(int, (self.integer, new.integer))
        else:
            comp1, comp2 = self.decimal, new.decimal
            used_decimal = True
            
        #Return if one is negative and the other isn't
        if not self.negative and new.negative:
            return greater_than
        elif self.negative and not new.negative:
            return less_than
        
        #Adjust the return values if the original number is negative
        greater_than += self.negative
        less_than -= self.negative
        
        #If a decimal, read both results from the front until one number is different
        if used_decimal:
            i = 0
            while True:
                try:
                    if comp1[i] < comp2[i]:
                        return less_than
                    elif comp1[i] > comp2[i]:
                        return greater_than
                except IndexError:
                    try:
                        comp1[i]
                    except IndexError:
                        try:
                            comp2[i]
                        except:
                            return equals
                        else:
                            return less_than
                    return greater_than
                i += 1
        
        #If an integer, just compare them normally
        if comp1 > comp2:
            return greater_than
        elif comp1 < comp2:
            return less_than
        return equals
        
        
    def __gt__(self, new):
        """Return if new number is greater than current number.
        
        Tests:
            >>> LargeNumber('123.456789012345') > '123.45678901234567'
            False
            >>> LargeNumber('123.456789012345') > '123.45678901234467'
            True
            >>> LargeNumber('-123.456789012345') > '-123.45678901234567'
            True
        """
        result = self._compare(new)
        return result == 1
    
    
    def __ge__(self, new):
        """Return if new number is greater than or equal to current number.
        
        Tests:
            >>> LargeNumber('123.456789012345') >= '123.45678901234567'
            False
            >>> LargeNumber('123.456789012345') >= '123.456789012345'
            True
            >>> LargeNumber('-123.456789012345') >= '-123.45678901234567'
            True
        """
        result = self._compare(new)
        return result in (1, 3)
        
        
    def __lt__(self, new):
        """Return if new number is less than current number.
        
        Tests:
            >>> LargeNumber('123.456789012345') < '123.45678901234567'
            True
            >>> LargeNumber('123.456789012345') < '123.45678901234467'
            False
            >>> LargeNumber('-123.456789012345') < '-123.45678901234567'
            False
        """
        result = self._compare(new)
        return result == 2
    
    
    def __le__(self, new):
        """Return if new number is less than or equal to current number.
        
        Tests:
            >>> LargeNumber('123.456789012345') <= '123.45678901234567'
            True
            >>> LargeNumber('123.456789012345') <= '123.456789012345'
            True
            >>> LargeNumber('-123.456789012345') <= '-123.45678901234567'
            False
        """
        result = self._compare(new)
        return result in (2, 3)


    def _add_subtract(self, new, reverse=False):
        """Handle any addition or subtraction between two LargeNumbers,
        without losing any precision.
        Use reverse to safely reverse the input number.
        
        Tests:
            >>> LargeNumber(2)._add_subtract(0.59381)
            LargeNumber('2.59381')
            >>> LargeNumber(-2.0002)._add_subtract(0.59381)
            LargeNumber('-1.40639')
            >>> LargeNumber(153153131351563643675375373)._add_subtract('1.00000072')
            LargeNumber('153153131351563643675375374.00000072')
            >>> LargeNumber(153153131351563643675375373)._add_subtract('-1.00000072')
            LargeNumber('153153131351563643675375371.99999928')
        """
        
        if not isinstance(new, LargeNumber):
            new = LargeNumber(new)
        else:
            new = new.copy()
            
        if reverse:
            new.negative = not new.negative
            new.refresh()
        
        integer = int(self.integer) * self.multiplier + int(new.integer) * new.multiplier
        
        #Add all decimals together
        decimal_list = []
        i = 0
        while True:
            total = 0
            strikes = 0
            try:
                total += int(self.decimal[i]) * self.multiplier
            except IndexError:
                strikes += 1
            try:
                total += int(new.decimal[i]) * new.multiplier
            except IndexError:
                strikes += 1
            if strikes == 2:
                break
            i += 1
            decimal_list.append(total)
        
        #Flatten out the decimal list
        integer_addition = 0
        for i in range(len(decimal_list)):
            index = -i - 1
            value = decimal_list[index]
            if not 0 <= value <= 9:
                try:
                    decimal_list[index - 1] += value // 10
                except:
                    integer_addition += value // 10
                decimal_list[index] %= 10
        integer += integer_addition
        decimal = ''.join(map(str, decimal_list)).rstrip('0')
        if not decimal:
            decimal = '0'
        
        #Add integer and decimal together if negative
        negative_override = False
        if integer < 0 and decimal != '0':
            integer += 1
            decimal = (1 - LargeNumber('0.' + decimal)).decimal
            if not integer:
                negative_override = True
        
        return LargeNumber('{}{}.{}'.format('-' if negative_override else '', integer, decimal))


    def __add__(self, new):
        """Perform an addition.
        
        Tests:
            >>> LargeNumber(50.59310) + 10050.92
            LargeNumber('10101.5131')
            >>> 10050.92 + LargeNumber(50.59310)
            LargeNumber('10101.5131')
            >>> LargeNumber(-50.59310) + 10050.92
            LargeNumber('10000.3269')
        """
        return self._add_subtract(new)
    __radd__ = __add__


    def __sub__(self, new):
        """Perform a subtraction.
        
        Tests:
            >>> LargeNumber(50.59310) - 10050.92
            LargeNumber('-10000.3269')
            >>> LargeNumber(-50.59310) - 10050.92
            LargeNumber('-10101.5131')
        """
        return self._add_subtract(new, reverse=True)


    def __rsub__(self, new):
        """Reverse the subtraction.
        
        Tests:
            >>> 10050.92 - LargeNumber(50.59310)
            LargeNumber('10000.3269')
            >>> 10050.92 - LargeNumber(-50.59310)
            LargeNumber('10101.5131')
        """
        return LargeNumber(-self)._add_subtract(new)
    
    
    def __mul__(self, new):
        """Multiply the current number by another.
        
        Tests:
            >>> LargeNumber(2) * LargeNumber(5)
            LargeNumber('10.0')
            >>> LargeNumber('2.72724') * LargeNumber('5.00921111')
            LargeNumber('13.6613209076364')
            >>> LargeNumber('-2.72724') * LargeNumber('5.00921111')
            LargeNumber('-13.6613209076364')
            >>> LargeNumber('-2.72724') * -LargeNumber('5.00921111')
            LargeNumber('13.6613209076364')
            >>> LargeNumber('272724.7992') * LargeNumber('500921111533578889.020000699827909933')
            LargeNumber('136613609558036106565338.7756444262110331104536')
        """
        if not isinstance(new, LargeNumber):
            new = LargeNumber(new)
        
        #Remove decimal points
        decimal_points = len(self.decimal) + len(new.decimal)
        self_total = self.integer + self.decimal
        new_total = new.integer + new.decimal
        
        #Add decimal points and sign
        result = power_of_10(int(self_total) * int(new_total), -decimal_points)
        if self.negative != new.negative:
            result.negative = True
            result.refresh()
        return result
    __rmul__ = __mul__
    
    
    def __floordiv__(self, new):
        """Perform a floor division.
        
        Tests:
            >>> LargeNumber(5) // LargeNumber(2)
            LargeNumber('2.0')
            >>> LargeNumber(765) // LargeNumber(2.6)
            LargeNumber('294.0')
            >>> LargeNumber(-765) // LargeNumber(2.6)
            LargeNumber('-295.0')
            >>> LargeNumber('764622642465.938553347537533') // LargeNumber('-2.6755135135153353201')
            LargeNumber('-285785378622.0')
        
        """
        result = LargeNumber(self, precision=1).__div__(new)
        if result.negative:
            result -= 1
        result.decimal = '0'
        return result
    
    
    def __rfloordiv__(self, new):
        """Reversed version of __floordiv__.
        
        Tests:
            >>> 1 // LargeNumber(500)
            LargeNumber('0.0')
            >>> -6 // LargeNumber(500.091, precision=12)
            LargeNumber('-1.0')
        """
        new = LargeNumber(new)
        new.precision = self.precision
        return new.__floordiv__(self)
    
    
    def __div__(self, new):
        """Divide the number by another.
        A max precision is set when creating the LargeNumber.
        If the end of the number is not reached and instead stopped by precision,
        the number will be marked as no longer exact.
        
        Tests:
            >>> LargeNumber('5') / LargeNumber('2')
            LargeNumber('2.5')
            >>> LargeNumber(765, precision=12) / LargeNumber(2.6)
            LargeNumber('294.2307692307692')
            >>> LargeNumber(-765, precision=12) / LargeNumber(2.6)
            LargeNumber('-294.2307692307692')
            >>> LargeNumber('764622642465.938553347537533', precision=50) / LargeNumber('-2.6755135135153353201')
            LargeNumber('-285785378621.133226089565313777724952105109839360081023850808361')
        """
        
        include_integers = False
        
        if not isinstance(new, LargeNumber):
            new = LargeNumber(new)
        else:
            new = new.copy()
        negative = self.negative
        
        #Disable negative for now as it'll mess bits up
        if new.negative:
            negative = not negative
            new.negative = False
            new.refresh()
        
        result = []
        
        remainder = LargeNumber('0')
        self_str = str(self)
        if self_str[0] == '-':
            self_str = self_str[1:]
            
        #Loop until max precision or full number is reached
        i = -1
        n = 0
        completed_number = False
        started = False
        markers = [False, False]
        while n <= self.precision + 1 and i < 200000:
            i += 1
            
            #Get the current value
            try:
                value = LargeNumber(self_str[i])
            except TypeError:
                value = self_str[i]
            except IndexError:
                value = LargeNumber('0')
                if str(remainder) == value:
                    completed_number = True
                    break
            
            #Add the decimal here, because it's super hard to figure out where it goes otherwise
            if n:
                n += 1
            if value == '.':
                markers[0] = True
                if not result:
                    result += [0, '.']
                else:
                    result.append('.')
                    n += 1
            
            #Use long division to get the next value
            else:
                current = value + remainder * 10
                temp = LargeNumber(str(new))
                count = 0
                while temp <= current:
                    count += 1
                    temp += new
                if count:
                    new_number = new * count
                    current -= new_number
                    result.append(count)
                    markers[1] = True
                elif result:
                    result.append(count)
                remainder = current
                
                if not n and all(markers):
                    n += 1
            
        #Flatten out the result list
        mark_for_delete = []
        for i in range(len(result)):
            index = -i - 1
            value = result[index]
            if value != '.' and not 0 <= value <= 9:
                offset = 1
                
                #Fix for if left most number overflows
                try:
                    if result[index - offset] == '.':
                        offset = 2
                except IndexError:
                    result = [0] + result
                    
                result[index - offset] += value // 10
                result[index] %= 10
        
        #Clean up the extra zeroes
        while not result[-1]:
            del result[-1]
        if result[-1] == '.':
            result.append(0)
            
        result = LargeNumber(('-' if negative else '') + ''.join(map(str, result)))
        if not completed_number:
            result.exact = False
        return result
        
    __truediv__ = __div__
    
    
    def __rtruediv__(self, new):
        """Reversed version of __truediv__.
        
        Tests:
            >>> 1 / LargeNumber(500)
            LargeNumber('0.002')
            >>> -6 / LargeNumber(500.091, precision=12)
            LargeNumber('-0.011997816397415')
        """
        new = LargeNumber(new)
        new.precision = self.precision
        
        return new.__div__(self)
    
    
    def __len__(self):
        """Get the length of the number (as a string).
        
        Tests:
            >>> len(LargeNumber('100.92'))
            6
            >>> len(LargeNumber(-100.0092))
            9
        """
        return len(str(self))
    
    
    def __abs__(self):
        """Return an absolute (positive) version of the number.
        
        Tests:
            >>> abs(LargeNumber('100.92'))
            LargeNumber('100.92')
            >>> abs(LargeNumber(-100.0092))
            LargeNumber('100.0092')
        """
        copy = LargeNumber(self)
        copy.negative = False
        copy.refresh()
        return copy
    
    
    def __getitem__(self, index):
        """Return a single item or slice of the number as it appears."""
        return str(self)[index]
    

    def __neg__(self):
        """Return a negative version of the number.
        
        Tests:
            >>> -LargeNumber(52.9)
            LargeNumber('-52.9')
            >>> -LargeNumber(-52.9)
            LargeNumber('52.9')
        """
        copy = LargeNumber(self)
        copy.negative = not copy.negative
        copy.refresh()
        return copy
    
    
    def __mod__(self, new):
        """Get the modulus of the number.
        This is a little inefficient as it does a floor division then multiplication.
        
        Not finished as it doesn't work with negative numbers, 
        I need to look into how it's supposed to work.
        
        Tests:
            >>> LargeNumber(172) % 100
            LargeNumber('72.0')
            >>> LargeNumber(-172) % 100
            LargeNumber('28.0')
            >>> LargeNumber(-172) % -100
            LargeNumber('-72.0')
            >>> LargeNumber(172) % 103.72
            LargeNumber('68.28')
            >>> LargeNumber(172.10948) % 103.72
            LargeNumber('68.38948')
            >>> LargeNumber(-172) % -100
            LargeNumber('-72.0')
        """
        if not isinstance(new, LargeNumber):
            new = LargeNumber(new)
        return self - new * (self // new)
            
        
    def copy(self):
        """Copy the class.
        
        Tests:
            >>> ln = LargeNumber(52)
            >>> ln.negative
            False
            >>> ln2 = ln
            >>> ln3 = ln.copy()
            >>> ln.negative = True
            >>> ln2.negative
            True
            >>> ln3.negative
            False
        """
        return LargeNumber(self)
    
    
    def __pow__(self, new):
        """Raise the current number to a power.
        A positive power will just multiply the number in a loop.
        A negative number will do the same, but is divided with 1.
        Decimal numbers are not supported yet, again I'm not sure how to do it.
        
        Tests:
            >>> LargeNumber(2) ** 3
            LargeNumber('8.0')
            >>> LargeNumber(5) ** 20
            LargeNumber('95367431640625.0')
            >>> LargeNumber(5.12) ** 20
            LargeNumber('153249554086588.8858358347027150309183618739122183602176')
            >>> LargeNumber(2) ** -2
            LargeNumber('0.25')
            >>> LargeNumber(-1609649.93, precision=12) ** -3
            LargeNumber('-0.00000000000000000023977599114892')
        """
        if not isinstance(new, LargeNumber):
            new = LargeNumber(new)
            
        if new.decimal != '0':
            raise NotImplementedError('unable to use decimal powers')
            '''
            #Approximation method (doesn't work)
            mid_point = self / 2
            step_size = mid_point.copy()
            for _ in range(4):
                step_size /= 2
                square_result = pow(mid_point, new.integer)
                if square_result == self:
                    raise IndexError('yeeeeeey')
                elif square_result > self:
                    mid_point -= step_size
                else:
                    mid_point += step_size
                print mid_point, square_result, new.integer
                
            #Maybe try figure out the long hand method: 
            #http://www.murderousmaths.co.uk/books/sqroot.htm
            '''
        
        #Negative power
        elif new.negative:
            result = LargeNumber(self)
            for i in range(int(new.integer) - 1):
                result *= self
            result.precision = self.precision
            return 1 / result
        
        #Power 0
        elif new.integer == '0':
            return LargeNumber(1)
        
        #Positive power
        else:
            result = LargeNumber(self)
            for i in range(int(new.integer) - 1):
                result *= self
            return result

    def format(self, decimals_max=11, exp_min=5, exp_max=11):
        """Format the number similar to how it would be with float().
        
        Tests:
            >>> LargeNumber('5003951.395159318573157888642').format()
            '5003951.39515931857'
            >>> (LargeNumber('5003951') * 35195.692).format()
            '1.76117518179e+11'
            >>> (LargeNumber('50039644512' * 100 + '.466') * 35195.692).format()
            '1.76117991605e+1104'
            >>> (LargeNumber(1) / LargeNumber(1098535358.30898532)).format()
            '9.10302970619e-10'
            >>> (LargeNumber(0.17) / LargeNumber('10985355358' * 50)).format()
            '1.54751480001e-550'
        """
        neg = '-' if self.negative else ''
        
        #If exponential options were chosen
        if exp_min and self.integer == '0' or exp_max and self.integer != '0':
            
            #Put whole number together
            total_number = (self.integer + self.decimal).strip('0').ljust(2, '0')
            if decimals_max is None:
                decimals_max = len(total_number)
                
            #Round last value
            new_decimals = total_number[1:decimals_max + 1]
            try:
                if int(total_number[decimals_max + 2]) >= 5:
                    new_decimals = new_decimals[:-1] + str(min(9, int(new_decimals[-1]) + 1))
            except IndexError:
                pass
            
            result = '{}{}.{}e'.format(neg, total_number[:1], new_decimals) + '{}{}'
            
            #Format value when a positive expoential
            exp_value = len(self.integer) - 1
            if exp_max is not None and self.integer != '0' and exp_value >= exp_max:
                return result.format('+', exp_value)
            
            #Format value when a negative exponential
            exp_value = len(self.decimal) - len(self.decimal.lstrip('0')) + 1
            if exp_min is not None and self.integer == '0' and exp_value >= exp_min:
                return result.format('-', exp_value)
        
        #Don't use exponents and just round the decimals
        if decimals_max is None:
            decimals_max = len(self.decimal)
        new_decimals = self.decimal[:decimals_max]
        try:
            if int(self.decimal[decimals_max]) >= 5:
                new_decimals = new_decimals[:-1] + str(min(9, int(new_decimals[-1]) + 1))
        except IndexError:
            pass
        return '{}{}.{}'.format(neg, self.integer, new_decimals)
    
    def __float__(self):
        """Return number as a float."""
        return float(str(self))
