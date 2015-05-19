from decimal import Decimal, getcontext


class NumberNames:
    """Build list of numbers from 0 to 10^3000."""
    
    #Name lists for 0 to 999
    num_units = ['zero','one','two','three','four','five','six','seven','eight','nine']
    num_teens = ['ten','eleven','twelve']+[i+'teen' for i in ['thir','four','fif']+num_units[6:]]
    num_tens = [i+('ty' if i[-1]!='t' else 'y') for i in ['twen','thir','for','fif']+num_units[6:]]
    
    #Name rules for 10^33 to 10^300
    num_exp_prefix = ['', 'un','duo','tre','quattor','quin','sex','septen','octo','novem']
    num_exp_amount = ['']+[i+'int' for i in ['vig','trig','quadrag','quinquag','sexag','septuag','octog','nonag']]
    
    #Name rules for 10^303 to 10^3000
    num_exp_units = [i+'illion' for i in ['m','b','tr','quadr','quint','sext','sept','oct','non']]
    num_exp_tens = [j+'illion' for j in ['dec']+num_exp_amount[1:]]
    num_exp_hundreds = ['']+[i+'en' for i in ['c','duoc','trec','quadring','quing','sesc','septing','octing','nong']]
    
    #Set up dictionary and manually add hundred and thousand which don't follow the rules
    num_dict = {}
    num_dict[2] = 'hundred'
    num_dict[3] = 'thousand'
    
    #Create Million through Nonillion (10^6 to 10^30)
    exp_current = 6
    for i in num_exp_units:
        num_dict[exp_current] = i
        exp_current += 3
        
    #Iterate through exponential hundreds (cen+)
    for prefix_hundreds in num_exp_hundreds:
        #Iterate through exponential tens (decillion+)
        for prefix_tens in num_exp_tens:
            #Iterate through exponential amounts (un, duo, tre, etc)
            for prefix in num_exp_prefix:
                num_dict[exp_current] = prefix_hundreds+prefix+prefix_tens
                exp_current += 3
        
        #Add 'tillion' before 'decillion' after the first run
        if not prefix_hundreds:
            num_exp_tens = ['tillion']+num_exp_tens

            
    #Add zero
    num_dict[0] = ''
    num_dict[-1] = ''


def remove_exponent(d):
    '''Remove exponent and trailing zeros.

    >>> remove_exponent(Decimal('5E+3'))
    Decimal('5000')

    '''
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


def num_to_text(input, as_digits=False, **kwargs):
    """Convert number between 0 and 999 to text"""
    
    use_fractions = kwargs.get('use_fractions', True)
    only_return_decimal = kwargs.get('only_return_decimal', False)
    fraction_precision = kwargs.get('fraction_precision', 100)
    negative_num = False
    
    #Fix for -0
    if isinstance(input, str):
        if input[0] == '-':
            input = input[1:]
            negative_num = True
    
    #Convert to float or int
    num_zeroes = 0
    input = str(input)
    
        
    #Get number of zeroes that are being removed to add again later
    no_zeroes = input
    if '.' in input:
        no_zeroes = input.rstrip('0')
        num_zeroes = len(input)-len(no_zeroes)
        
        #Fix number of zeros being 1 too high if all decimal points = 0
        if no_zeroes[-1] == '.':
            num_zeroes -= 1
            no_zeroes += '0'
    
    input = Decimal(no_zeroes)
   
    #Make sure number is positive
    if input < 0:
        input = input*-1
        negative_num = True
        
    #If only integers should be returned
    if as_digits:
        
        output = str(input)+'0'*num_zeroes
        if '.' in output:
            
            '''
            #Fix for when input doesn't contain a decimal
            if '.' not in str(input):
                output = str(input)+'.'+'0'*num_zeroes
                '''
                
            #Attempt to calculate fraction of decimal point
            fraction_output = find_fraction(float(output), fraction_precision)
            if fraction_output and use_fractions:
                fraction_suffix = get_fraction_suffix(*fraction_output)
                fraction_prefix = ''
                if not only_return_decimal:
                    fraction_prefix = ' and '
                return '{p}{0}/{1}{s}'.format(*fraction_output, s=fraction_suffix, p=fraction_prefix)
            else:
                #Return decimal points if 0.x
                if only_return_decimal:
                    return '.'+str(output.split('.')[1])
                #Return number with decimals if not between 0 and 1
                else:
                    return str(output)
        
        
        #Re-add the negative sign
        if negative_num:
            output = '-' + output
            
        return output
    
    #If number out of range, recursively use LargeNumber
    if 0 > input or input > 999:
        print "Warning: Number out of range."
        return LargeNumber(input, as_digits).full()
    
    #Break down number into separate parts
    output_hundreds = int(input/100)
    output_tens = int((input%100)/10)
    output_units = int(input%10)
    output_decimals = str(input).split('.')
    
    #Fill output decimals with extra zeroes
    if len(output_decimals)>1:
        output_decimals[1] += '0'*num_zeroes
    
    output_text = ''
    #If number is negative
    if negative_num:
        output_text += 'negative '
    #If number is above 100
    if output_hundreds:
        output_text += NumberNames.num_units[output_hundreds] + ' hundred'
    #If last 2 digits are above 10
    if output_tens:
        if output_hundreds:
            output_text += ' and '
        if output_tens != 1:
            output_text += NumberNames.num_tens[output_tens-2]
        else:
            output_text += NumberNames.num_teens[output_units]
    #If last digit is above 0
    if output_units:
        #If last two digits are not between ten and nineteen (added in the tens)
        if output_tens != 1:
            if output_tens:
                output_text += '-'
            elif output_hundreds:
                output_text += ' and '
            output_text += NumberNames.num_units[output_units]
    #Add a zero
    if not (output_hundreds or output_tens or output_units) and not only_return_decimal:
        output_text += NumberNames.num_units[output_units]
        
    #Add the decimal points
    if len(output_decimals)>1:
        output_text += ' point'
        #Remove 'zero' if 'zero point x'
        '''
        if only_return_decimal:
            if output_text[:4] == NumberNames.num_units[0]:
                output_text = output_text[4:]
                '''
        #Write list of decimals
        for i in output_decimals[1]:
            output_text += ' '+NumberNames.num_units[int(i)]
            
    return output_text

def find_matching_exp(input, all_available_numbers):
    """Iterate through list of numbers to find the lowest match."""
    for i in xrange(len(all_available_numbers)):
        try:
            if input < all_available_numbers[i+1]:
                return all_available_numbers[i]
        #If number is higher than max index
        except IndexError:
            return all_available_numbers[i]
       
def find_fraction(input, precision):
    """Convert a decimal into a fraction if possible.
    
    Will check up to the value of precision, so a precision of 10 will not find 1/11th or below.
    Recommended to use 100, but no more.
    
    Complexity is the sum of 0 to precision, so be careful as higher values exponentially take longer.
    """
    for j in xrange(2, precision+1):
        j = float(j)
        for i in xrange(1, int(j)):
            if i/j == input:
                return int(i), int(j)

            
def get_fraction_suffix(x, y):
    """Calculate fraction suffix based on numerator (x) and denominator (y).
    Will use plural if numerator is above 1.
    
    >>> get_fraction_suffix(1, 3)
    'rd'
    >>> get_fraction_suffix(1, 4)
    ''
    >>> get_fraction_suffix(1, 5)
    'th'
    >>> get_fraction_suffix(2, 11)
    'ths'
    >>> get_fraction_suffix(1, 21)
    'st'
    """
    
    #Convert to str and get important characters
    y = str(y)
    x = str(x)
    last_num = y[-1]
    try:
        second_num = y[-2]
    except IndexError:
        second_num = 0
    
    #Define rules
    if y == '1':
        suffix = ''
    elif last_num == '3':
        suffix = 'rd'
    elif second_num == '1':
        suffix = 'th'
    elif last_num == '2':
        if second_num:
            suffix = 'nd'
        else:
            suffix = ''
    elif last_num == '4' and not second_num:
        suffix = ''
    elif last_num == '1':
        suffix = 'st'
    else:
        suffix = 'th'
    
    #Make plural if x is above 1
    if x not in ('1', '0') and suffix:
        suffix += 's'
        
    return suffix   
           


def format_input(input):
    """Format the input to remove spaces and new lines.
    Also set the precision to the length of the input, as too low
    can cause errors with calculations on large numbers.
    
    Returns the number in Decimal() format.
    
    >>> format_input(4264.425)
    Decimal('4264.425')
    
    >>> format_input('''
    ... 1 000 000 000
    ... 000 000 000
    ... ''')
    Decimal('1000000000000000000')
    """
    input = str(input).replace(" ","").replace("\n","")
    getcontext().prec = max(28, len(input))
    return Decimal(input)

def round_with_precision(input, num_decimals=None, force_decimals=True, force_decimals_when_none=False):
    
    input = Decimal(input)
    
    #Accurately round the number
    if num_decimals is not None:
        
        #Increase the precision to stop errors on large num_decimals values
        current_context = getcontext().prec
        getcontext().prec = max(current_context, num_decimals*1.1)
        
        if num_decimals:
            input = input.quantize(Decimal('0.'+'0'*(num_decimals-1)+'1'))
        else:
            input = input.quantize(Decimal('1'))
        input = Decimal(str(input).rstrip('0'))
        
        getcontext().prec = current_context
        
    
    input = str(input)
    #ends_in_zero = input != input.rstrip('0')
    
        
    if force_decimals:
        
        #Convert output to string and fill in decimals
        if '.' not in input:
            if num_decimals is not None:
                input += '.'+'0'*num_decimals
            else:
                input += '.0'
            
        elif num_decimals is not None:
            current_decimals = len(input.split('.')[1])
            input += '0'*(num_decimals-current_decimals)
    
    #Trim decimal places if not forcing decimals
    if not force_decimals or not force_decimals_when_none:
        input = input.rstrip('0')
        if input[-1] == '.':
            input += '0'
            
    return input


class LargeNumber(Decimal):
    
    def __init__(self, input, **kwargs):
        
        #Copy over class objects from decimal
        Decimal.__init__(input)
        '''
        To do: add custom functions to output LargeNumber instead of Decimal
        add, subtract, multiply, etc
        '''
        
        self.input = format_input(input)
        self.as_digits = kwargs.get('digits', True)
        self.all_available_numbers = tuple(sorted(NumberNames.num_dict.keys()))
    
    def __repr__(self):
        """Return class with number."""
        
        #Remove the exponent if a large int/float value is input
        #Squared length seems to work but increase if error
        if 'E+' in str(self.input):
            original_precision = getcontext().prec
            getcontext().prec = len(str(self.input))**2
            formatted_input = remove_exponent(self.input)
            getcontext().prec = original_precision
        else:
            formatted_input = self.input
            
        return "LargeNumber('{}')".format(formatted_input)
    
    def _calculate_number_parts(self, **kwargs):
        """Convert a number to it's full text representation.
        
        full_number(input, as_digits, kwargs):
            input: 
                Number to use.
                It can be in any format as long as it can be converted to Decimal.
            as_digits: 
                If the amounts should be kept as integers or not
                True:
                    450 million and 20
                False:
                    four hundred and fifty million and twenty
                If the number is higher than the maximum number (10^3000), it is recommended to set to True).
            kwargs:
                use_fractions:
                    Will only work if as_digits is set to True.
                    Determine if decimal points should be converted to fractions if possible.
                    Fractions will contain prefixes, such as 1/3rd or 7/25ths.
                    Default: True
                fraction_precision:
                    Range to look for a fraction.
                    Set to maximum denominator, where it'll search up until that point.
                    Default: 100
        
        
        >>> input = 10000503.125
        
        >>> full_number(input, False)
        'ten million, five hundred and three point one two five'
        
        >>> full_number(-input, False)
        'negative ten million, five hundred and three point one two five'
        
        >>> full_number(input, True)
        '10 million, 5 hundred and 3 and 1/8th'
        
        >>> full_number(-input, True, use_fractions=False)
        '-10 million, 5 hundred and 3 point 125'
        """
        """Convert a number to a general text representation.
        
        simple_number(input, min_amount, num_decimals, force_decimals):
            input: 
                Number to use.
                It can be in any format as long as it can be converted to Decimal.
            min_amount:
                Minimum amount required to move up a value.
                It works on a log scale, but may be any value.
                Example:
                    If you have 1 million, the current value is 1.
                    By default, you will go up to 999 thousand, then move to 1 million,
                    because 999 thousand is 0.999 million, and under 1.
                    However, set min_amount to 0.1, and it will switch to 0.1 million from 99 thousand.
                    Set min_amount to 10, and to reach 10 million, it will go up to 9999 thousand.
                    Set min_amount to 5, and it will move from 4999 thousand to 5 million.
            num_decimals:
                Number of decimal points to round to.
            force_decimals:
                If the number of decimal points should be fixed.
                True:
                    5.3 million
                    2 thousand
                    7.64 billion
                False:
                    5.30 million
                    2.00 thousand
                    7.64 billion
        
        
        Example with decimal forcing
        >>> input = 10000503.125
        
        Conversion with default settings
        >>> simple_number(input)
        '10.00 million'
        
        Conversion without forcing decimals
        >>> simple_number(input, force_decimals=False)
        '10 million'
        
        
        Example with changing min_amount
        >>> input = 54321
        
        Conversion with default minimum amount
        >>> simple_number(input, 1)
        '54.32 thousand'
        
        Conversion with low minimum amount
        >>> simple_number(input, 0.1)
        '0.05 million'
        
        Conversion with high minimum amount
        >>> simple_number(input, 10)
        '543.21 hundred'
        
        Conversion with minimum amount slightly below input
        >>> simple_number(input, 0.5)
        '0.05 million'
        
        Conversion with minimum amount slightly above input
        >>> simple_number(input, 0.6)
        '54.32 thousand'
        
        Example with text
        >>> simple_number(input, 1, False)
        'fifty-four point three two thousand'
        """
        max_iterations = kwargs.get('max_iterations', None)
        num_decimals = kwargs.get('num_decimals', 3)
        force_decimals = kwargs.get('force_decimals', True)
        force_decimals_when_none = kwargs.get('force_decimals_when_none', True)
        
        min_amount = Decimal(str(kwargs.get('min_amount', 1)))
        
        #If more than one iteration, set the min amount to 1 otherwise you get an infinite loop
        if max_iterations and min_amount < 1:
            min_amount = Decimal('1')
        min_offset = min_amount.logb()
        
        input = self.input
        num_output = {}
        num_exp = 1
        first_run = True
        
        max_steps = 1
       
        
        #Get multiplier from the min_amount variable
        min_amount_multiplier = Decimal(('%.2E'%min_amount).split('E')[0])
        
        #Match values to exponentials
        while num_exp > 0 and (input >= 1 or first_run):
            
            first_run = False
            
            #Figure which name to use
            if input:
                num_digits = (input/min_amount_multiplier).logb()
            else:
                #Fix to stop logb() error if input is zero
                num_digits = Decimal(1).logb()
                
            num_digits -= min_offset
            num_exp = find_matching_exp(num_digits, self.all_available_numbers)
            
            #Fix when given a high min_amount value that pushes num_exp below 0
            if num_exp <= 0:
                num_exp = 0
            
            #Fix for values between 0 and 1
            if -1 < input < 1:
                num_exp = 0
                
            #Get matching amount 
            current_multiplier = pow(Decimal(10), Decimal(num_exp))
            current_output = input/current_multiplier
            
            #Add to output
            if len(num_output)+1 > max_iterations and max_iterations is not None:
                
                current_output = round_with_precision(current_output, num_decimals, force_decimals, force_decimals_when_none)
                num_output[num_exp] = (str(current_output))
                input = 0
                break
                
            else:
                
                #Continue
                num_output[num_exp] = (str(current_output).split('.')[0])
                input = input%pow(Decimal(10), Decimal(num_exp))
            
            #Make number positive after first run
            if input < 0:
                input *= -1
        
        num_output[-1] = input
        
        return num_output

    
    def to_text(self, **kwargs):
        
        use_fractions = kwargs.get('use_fractions', True)
        fraction_precision = kwargs.get('fraction_precision', 100)
        
        num_decimals = kwargs.get('num_decimals', None)
        max_decimals = kwargs.get('max_decimals', None)
        force_decimals = kwargs.get('force_decimals', True)
        force_decimals_when_none = kwargs.get('force_decimals_when_none', False)
        
        as_digits = kwargs.get('digits', True)
        
        num_name = []
        num_name_joined = ''
        num_output = self._calculate_number_parts(**kwargs)
        
        #Get remaining decimals for later and remove from output
        remaining_decimals = num_output.pop(-1)
        
        #Fix for values between 0 and 1
        if not num_output:
            num_output[0] = 0
        
        #Convert numbers to words
        for i in sorted(num_output.keys())[::-1]:
            current_value = num_output[i]
            additional_value = ''
            if NumberNames.num_dict[i]:
                additional_value = ' '+NumberNames.num_dict[i]
            
            #Avoid using fractions if prefix (eg. 0.5 billion not 1/2 billion)
            should_use_fractions = use_fractions
            if i:
                should_use_fractions = False
                if force_decimals_when_none:
                    
                    #Force decimals when there are no initial decimals, to stop things like 65 million0.0
                    force_decimals_when_none = False
                    if num_decimals is not None:
                        
                        #Check if existing decimal points (fixes things like 46.500.000 million)
                        current_num_decimals = 0
                        if '.' in current_value:
                            current_num_decimals = len(current_value.split('.')[1])
                        else:
                            current_value += '.'
                        required_decimals = max(0, num_decimals-current_num_decimals)
                        current_value += '0'*required_decimals
                        
                    else:
                        current_value += '.0'
                
            
            text_num = num_to_text(current_value, as_digits, 
                                   use_fractions=should_use_fractions, 
                                   fraction_precision=fraction_precision) + additional_value
            
            #Fix for min_amount under 0
            if i and current_value[:10] == 'zero point':
                text_num = text_num[5:]
                
            num_name.append(text_num)
        
        #Join list
        if len(num_name)-1:
            num_name_joined += ', '.join(num_name[:-1]) + ' and '
        num_name_joined += num_name[-1]
        
        #Add decimal point
        if remaining_decimals or force_decimals_when_none:
            
            if not remaining_decimals:
                remaining_decimals = '0.'
                if num_decimals is not None:
                    remaining_decimals += '0'*num_decimals
                else:
                    remaining_decimals += '0'
            
            #Convert to text
            remaining_decimals = round_with_precision(remaining_decimals, num_decimals, force_decimals, force_decimals_when_none)
                            
            decimal_num = num_to_text(remaining_decimals, as_digits, 
                                      use_fractions=use_fractions, 
                                      fraction_precision=fraction_precision,
                                      force_decimals_when_none=force_decimals_when_none,
                                      only_return_decimal=True)
            
            #Fix to stop fractions not removing a zero (eg. 0 and 2/5ths should be 2/5ths)
            if '/' in decimal_num:
                if num_name_joined and num_name_joined != '0':
                    num_name_joined += ' and '
                else:
                    num_name_joined = ''
                
            num_name_joined += decimal_num
        
        return num_name_joined
        
    def quick(self, num_decimals=3):
        """Quickly format the number."""
        kwargs = {}
        kwargs['max_iterations'] = 0
        kwargs['num_decimals'] = num_decimals
        kwargs['force_decimals_when_none'] = True
        kwargs['use_fractions'] = False
        kwargs['digits'] = True
        return self.to_text(**kwargs)
