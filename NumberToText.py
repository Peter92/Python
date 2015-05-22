"""This script is for converting a number into it's text representation, and currently contains
all the values up to 10^3000. It can go further, but will reuse old values once the limit is
hit (eg. 999 nongennovemnonagintillion to 1 thousand nongennovemnonagintillion).

It is recommended you input numbers as strings or in Decimal format, since Python integers
and floats don't have enough precision, and the output won't be what is expected.


LargeNumber(number).to_text() is the main function, though LargeNumber(number).quick() can be
used to easily get a single number with it's prefix.

A few parameters can be input to change the output, the main useful ones being max_iterations
and digits. See the to_text() function for more detailed descriptions and examples of them
in use.

kwargs:
    digits:
        Default: False
        If the number should be entirely text, or use a mix of digits and text.
    num_decimals:
        Default: None
        Number of decimals to display. None shows all of them.
    force_decimals:
        Default: False
        Force the number of decimals to equal num_decimals.
        If num_decimals is None, make sure each number is a decimal value.
    min_decimals:
        Default: -1
        Minimum amount of decimals to give each number.
        Needs force_decimals enabled to work.
    max_iterations:
        Default: -1
        Maximum number of iterations to use when calculating the number.
        For example, '1.35 thousand' is 0 iterations, '1 thousand and 3.52 hundred' is 1 iteration,
        and '1 thousand, 3 hundred and 52' is 3 iterations.
    min_amount:
        Default: 1
        Minimum amount of an exponential a number can be.
        For example, a min_amount of 0.1 means '1 hundred' will be turned to '0.1 thousand'.
    min_amount_limit:
        Default: -1
        How many iterations to apply min_amount to.
        0 iterations has no effect on output.
    use_fractions:
        Default: False
        If fractions should be calculated.
        Only used if digits is enabled since their text representation is a lot harder to code.
    fraction_precision:
        Default: 100
        Determines how many calculations are done to find a fraction before giving up.
        The value of 100 means 0.01 to 0.99 all have valid fractions.
        
In the descriptions, I use 'prefix' and 'exponential value' or 'suffix', due to no idea of what
to actually use. By suffix or exponential, I mean the name that comes after the number, such as
'thousand' or 'trillion', and the prefix is the number that relates to these.
"""

from decimal import Decimal, getcontext
class NumberNames:
    """Build list of numbers from 0 to 10^3000.
    Would do more but I couldn't find the rules for above 3000.
    
    Functions:
        all_available_numbers:
            Not a function, but returns the list of every number suffix.
        num_to_text:
            Convert number between 0 and 999 to text.
    """
    
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
    
    all_available_numbers = tuple(sorted(num_dict.keys()))
    
    @classmethod
    def num_to_text(self, input=0, as_digits=False, **kwargs):
        """Convert number between -999 and 999 to text.
        It can convert higher numbers, but will use recursion on LargeNumber().to_text() to do so.
        
        Parameters:
            input: 
                Number between 0 and 999 to convert.
                
            as_digits:
                Default: False
                See LargeNumber().to_text()
            
            kwargs:                    
                only_return_decimal:
                    Default: False
                    If it should only return the decimal place, or full number.
                    Mainly used to make the text formatting a little easier.
                
                print_warning:
                    Default: False
                    Prints a warning when a number goes out of range and recursion is used.
                    The prefix to the highest exponential will have the code run on it again, so while it will be
                    technically correct, it can be confusing to read.
                    
                use_fractions:
                    Default: True
                    See LargeNumber().to_text()
                 
                fraction_precision:
                    Default: 100
                    See LargeNumber().to_text()
        
        
        General Examples:
            >>> NumberNames.num_to_text()
            'zero'
            >>> NumberNames.num_to_text(999)
            'nine hundred and ninety-nine'
            >>> NumberNames.num_to_text(-999)
            'negative nine hundred and ninety-nine'
            >>> NumberNames.num_to_text(9999)
            'nine thousand, nine hundred and ninety-nine'
            >>> NumberNames.num_to_text(9999, print_warning=True)
            Warning: Number out of range!
            'nine thousand, nine hundred and ninety-nine'
            >>> NumberNames.num_to_text(572.5)
            'five hundred and seventy-two point five'
            >>> NumberNames.num_to_text(572.5, True)
            '572 and 1/2'
            >>> NumberNames.num_to_text(572.5, True, use_fractions=False)
            '572.5'
            >>> NumberNames.num_to_text(572.5, True, only_return_decimal=True)
            '1/2'
            >>> NumberNames.num_to_text(572.5, True, use_fractions=False, only_return_decimal=True)
            '.5'
            >>> NumberNames.num_to_text(572.5, False, only_return_decimal=True)
            'point five'
        
        """
        
        use_fractions = kwargs.get('use_fractions', True)
        only_return_decimal = kwargs.get('only_return_decimal', False)
        fraction_precision = kwargs.get('fraction_precision', 100)
        print_warning = kwargs.get('print_warning', False)
        
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
            
            #Re-add the negative sign
            if negative_num:
                output = '-' + output
                
            if '.' in output:
                
                #Split output for when it's been combined with another exponential value (must be between 0 and 1)
                decimal_output = '0.'+output.split('.')[1]
                
                #Attempt to calculate fraction of decimal point
                fraction_output = CalculateFraction.find(float(decimal_output), fraction_precision)
                if fraction_output and use_fractions:
                    fraction_suffix = CalculateFraction.suffix(*fraction_output)
                    fraction_prefix = ''
                    
                    #Add prefix if not only returning the decimal
                    if not only_return_decimal:
                        fraction_prefix = output.split('.')[0]+' and '
                    
                    return '{p}{0}/{1}{s}'.format(*fraction_output, s=fraction_suffix, p=fraction_prefix)
                    
                else:
                    #Return decimal points if 0.x
                    if only_return_decimal:
                        return '.'+str(output.split('.')[1])
                    #Return number with decimals if not between 0 and 1
                    else:
                        return str(output)
            
            return output
        
        #If number out of range, recursively use LargeNumber
        if 0 > input or input > 999:
            if print_warning:
                print "Warning: Number out of range!"
            return LargeNumber(input).to_text(digits=as_digits)
        
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
            output_text += self.num_units[output_hundreds] + ' hundred'
        #If last 2 digits are above 10
        if output_tens:
            if output_hundreds:
                output_text += ' and '
            if output_tens != 1:
                output_text += self.num_tens[output_tens-2]
            else:
                output_text += self.num_teens[output_units]
        #If last digit is above 0
        if output_units:
            #If last two digits are not between ten and nineteen (added in the tens)
            if output_tens != 1:
                if output_tens:
                    output_text += '-'
                elif output_hundreds:
                    output_text += ' and '
                output_text += self.num_units[output_units]
        #Add a zero
        if not (output_hundreds or output_tens or output_units) and not only_return_decimal:
            output_text += self.num_units[output_units]
            
        #Add the decimal points
        if len(output_decimals)>1:
            output_text += ' point'
            if only_return_decimal:
                output_text = 'point'
            
            #Write list of decimals
            for i in output_decimals[1]:
                output_text += ' '+self.num_units[int(i)]
                
        return output_text


class CalculateFraction(object):
    """Class containing functions for calculating fractions.
    Can find the numberator and denominator, and calculate the suffix based on those values.
    
    Functions:
        find: 
            Convert a decimal value into fraction.
        suffix: 
            Calculate suffix for fraction.
    """

    @staticmethod
    def find(input, precision=100):
        """Convert a decimal into a fraction if possible.
        
        Will check up to the value of precision, so a precision of 10 will not find 1/11th or below.
        Recommended to use 100, but no more.
        Uses float so isn't too precise, as using Decimal is noticeably slower.
        
        Complexity is the sum of 0 to precision, so be careful as higher values exponentially take longer.
        
        Parameters:
            input:
                Floating point number to find fraction of.
            
            precision:
                Default: 100
                Maximum number of calculations to do.
                The calculation time increases exponentially, as the number of iterations is the sum of
                one to precision. (eg. precision 100 is sum(range(100)) or 4950 calculations)
        
        >>> CalculateFraction.find(0.5)
        (1, 2)
        >>> CalculateFraction.find('0.3')
        (3, 10)
        >>> CalculateFraction.find(1.0/4.0, 4)
        (1, 4)
        >>> CalculateFraction.find(1.0/4.0, 3)
        >>> CalculateFraction.find(5.5)
        (6, 2)
        >>> CalculateFraction.find(5)
        """
        
        #Convert to float
        if not isinstance(input, float):
            input = float(input)
            
        #Make sure it is between 0 and 1
        original_input = int(input)+1
        if not (0 < input < 1):
            input = input%1
            
        #Loop through all calculations until a match is found
        for j in xrange(2, precision+1):
            j = float(j)
            for i in xrange(1, int(j)):
                if i/j == input:
                    return i*original_input, int(j)
    
    @staticmethod
    def suffix(x, y):
        """Calculate fraction suffix based on numerator (x) and denominator (y).
        Will use plural if numerator is above 1.
        
        >>> CalculateFraction.suffix(1, 3)
        'rd'
        >>> CalculateFraction.suffix(1, 4)
        ''
        >>> CalculateFraction.suffix(1, 5)
        'th'
        >>> CalculateFraction.suffix(2, 11)
        'ths'
        >>> CalculateFraction.suffix(1, 21)
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



class LargeNumber(Decimal):
    """Convert any number of any precision into text.
    
    Functions:
        to_text:
            Convert a number into text.
        quick:
            Automatically sets some values and runs to_text().
        format_input:
            Convert the input into decimal format and set precision.
        remove_exponent:
            Remove an exponent from a Decimal value.
        _round_with_precision:
            Accurate way of rounding between 0 and 1.
        _find_matching_exp:
            Find the nearest low exponential value.
        _calculate_number_parts:
            Split a number into separate exponentials.
    """
    
    def __init__(self, input, **kwargs):
        
        #Copy over class objects from decimal
        Decimal.__init__(input)
        '''
        To do: add custom functions to output LargeNumber instead of Decimal
        add, subtract, multiply, etc
        '''
        self.input = self.format_input(input, True)
        self.all_available_numbers = NumberNames.all_available_numbers
    
    def __repr__(self):
        """Return class with number."""
        
        #Remove the exponent if a large int/float value is input
        #Squared length seems to stop precision errors but increase if error happens
        if 'E+' in str(self.input):
            original_precision = getcontext().prec
            getcontext().prec = len(str(self.input))**2
            formatted_input = self.remove_exponent(self.input)
            getcontext().prec = original_precision
        else:
            formatted_input = self.input
            
        return "LargeNumber('{}')".format(formatted_input)
    
    @staticmethod
    def format_input(input, set_prec=False):
        """Format the input to remove spaces and new lines.
        Also set the precision to the length of the input, as too low
        can cause errors with calculations on large numbers.
        
        Returns the number in Decimal() format.
        
        Parameters:
            input:
                Number or string to convert to Decimal value.
                
            set_prec:
                If the precision should be set.
                The LargeNumber class needs this doing, but for general use there's no need.
        
        >>> LargeNumber.format_input(4264.425)
        Decimal('4264.425')
        >>> LargeNumber.format_input('''
        ... 1 000 000 000
        ... 000 000 000
        ... ''')
        Decimal('1000000000000000000')
        """
        input = str(input).replace(" ","").replace("\n","")
        getcontext().prec = max(28, len(input))
        return Decimal(input)
    
    @staticmethod
    def _round_with_precision(input, num_decimals=None, force_decimals=False):
        """Accurately round a number between 0 and 1. 
        Used because the round() function doesn't have enough precision.
        If the output number is rounded and has zeroes at the end, trim the zeroes only if the 
        output number is different from the input, otherwise keep the zeroes.
         
        Parameters:
            
            input:
                Value to round.
                Will only work if value is between 0 and 1, although it won't throw an error otherwise.
                Recommended to input as string or Decimal format, as to not lose precision.
                
            num_decimals:
                Default: None
                See LargeNumber().to_text()
                    
            force_decimals:
                Default: False
                See LargeNumber().to_text()
        
        >>> LargeNumber._round_with_precision(0.3)
        '0.3'
        >>> LargeNumber._round_with_precision(0.54201530)
        '0.5420153'
        >>> LargeNumber._round_with_precision(0.54201530, num_decimals=3)
        '0.542'
        >>> LargeNumber._round_with_precision(0.54201530, num_decimals=4)
        '0.5420'
        >>> LargeNumber._round_with_precision(0.54200000, num_decimals=4)
        '0.542'
        >>> LargeNumber._round_with_precision(0.54200001, num_decimals=4)
        '0.5420'
        >>> LargeNumber._round_with_precision(1)
        '1.0'
        """
        input = str(input)
        if '.' in str(input):
            original_input = input.rstrip('0')
        else:
            original_input = input+'.0'
        input = Decimal(original_input)
        
        #Accurately round the number
        if num_decimals is not None:
            
            #Increase the precision to stop errors on large num_decimals values
            current_context = getcontext().prec
            getcontext().prec = max(current_context, num_decimals*1.1)
            if num_decimals:
                input = input.quantize(Decimal('0.'+'0'*(num_decimals-1)+'1'))
            else:
                input = input.quantize(Decimal('1'))
            getcontext().prec = current_context
        input = str(input)
        
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
        
        #Trim decimal places if not forcing decimals, and if decimal places haven't been cut off
        # eg. 70500 = 70.5 thousand, no matter the decimal places
        # however, 70500.005 = 70.500005, or to 3 decimal places is 70.500 thousand
        if not force_decimals and original_input == input.rstrip('0'):
            input = input.rstrip('0')
            if input[-1] == '.':
                input = input[:-1]
                
        return input
    
    @classmethod
    def remove_exponent(self, input):
        '''Remove exponent of a Decimal value. 
        If input is in the wrong format, code will run again with the converted input.
    
        >>> LargeNumber.remove_exponent(Decimal('5E+3'))
        Decimal('5000')
        >>> LargeNumber.remove_exponent(5000)
        Decimal('5000')
        '''
        try:
            if input == input.to_integral():
                return input.quantize(Decimal(1))
            else:
                return input.normalize()
        except AttributeError:
            return self.remove_exponent(self.format_input(input))
    
    @staticmethod
    def _find_matching_exp(input, all_available_numbers):
        """Iterate through list of numbers to find the nearest low match.
        
        Parameters:
            input:
                Calculated exponential value
                
            all_available_numbers:
                All exponential values
                
        
        >>> all_available_numbers = NumberNames.all_available_numbers
        >>> LargeNumber._find_matching_exp(4, all_available_numbers)
        3
        >>> LargeNumber._find_matching_exp(643, all_available_numbers)
        642
        >>> LargeNumber._find_matching_exp(10000, all_available_numbers)
        3000
        >>> LargeNumber._find_matching_exp(-47, all_available_numbers)
        -1
        """
        for i in xrange(len(all_available_numbers)):
            try:
                #Return first match
                if input < all_available_numbers[i+1]:
                    return all_available_numbers[i]
            #If number is higher than max index
            except IndexError:
                return all_available_numbers[i]
    
    def _calculate_number_parts(self, **kwargs):
        """Used by to_text() for calculating the output. Returns dictionary of numbers matching their exponential.
        The exponentials are calculated from the NumberNames class.
        
        Parameters:
            kwargs:
                min_amount:
                    Default: 1
                    See LargeNumber().to_text()
                    
                min_amount_limit:
                    Default: -1 (infinite)
                    See LargeNumber().to_text()
                    
                max_iterations:
                    Default: -1 (infinite)
                    See LargeNumber().to_text()
                    
                num_decimals: 
                    Default: None
                    See LargeNumber().to_text()
                    
                force_decimals:
                    Default: None 
                    See LargeNumber().to_text()
                    
        
        Output examples:
        key:value relates to value*(10^key), aside from when the key is -1, in which the value is the decimal remainder.
            >>> LargeNumber(5000)._calculate_number_parts()
            {3: '5', -1: '0'}
            >>> LargeNumber(-123456)._calculate_number_parts()
            {0: '56', 2: '4', 3: '-123', -1: '0'}
            >>> LargeNumber("100.72")._calculate_number_parts()
            {2: '1', -1: '0.72'}
        """
        max_iterations = kwargs.get('max_iterations', -1)
        num_decimals = kwargs.get('num_decimals', None)
        force_decimals = kwargs.get('force_decimals', False)
        
        min_amount = Decimal(str(kwargs.get('min_amount', 1)))
        min_amount_limit = Decimal(str(kwargs.get('min_amount_limit', -1)))
        
        #If more than one iteration, set the min amount to 1 otherwise you get an infinite loop
        if max_iterations and min_amount < 1:
            min_amount = Decimal('1')
            
        min_offset = min_amount.logb()
        
        input = self.input
        num_output = {}
        num_exp = 1
        first_run = True       
        
        #Get multiplier from the min_amount variable
        min_amount_multiplier = Decimal(('%.2E'%min_amount).split('E')[0])
        
        #Match values to exponentials
        count = 0
        while num_exp > 0 and (input >= 1 or not count):
            
            #Reset min_amount to default
            if count == min_amount_limit:
                min_offset = Decimal('1').logb()
            count += 1
            
            #Figure which name to use
            if input:
                num_digits = (input/min_amount_multiplier).logb()
            else:
                #Fix to stop logb() error if input is zero
                num_digits = Decimal(1).logb()
                
            num_digits -= min_offset
            num_exp = self._find_matching_exp(num_digits, self.all_available_numbers)
            
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
            if len(num_output)+1 > max_iterations and max_iterations >= 0:
                current_output = self._round_with_precision(current_output, num_decimals, force_decimals)
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
                
        num_output[-1] = str(input)
        
        #Re-run the code if only one iteration is output (basically a fix for low min_amount not working)
        if len(num_output) == 2 and min_amount != Decimal(str(kwargs.get('min_amount', 1))) and max_iterations != 0:
            kwargs['max_iterations'] = 0
            num_output = self._calculate_number_parts(**kwargs)
        
        return num_output

    
    def to_text(self, **kwargs):
        """Convert the number to a text representation.
        
        Parameters:
            kwargs:
                digits:
                    Default: True
                    If the output should be text and digits or just text (53 thousand or fifty-three thousand).
                    
                    >>> LargeNumber(7654321.5).to_text(digits=True)
                    '7 million, 654 thousand, 3 hundred and 21.5'
                    >>> LargeNumber(7654321.5).to_text(digits=False)
                    'seven million, six hundred and fifty-four thousand, three hundred and twenty-one point five'
                    
                min_amount:
                    Default: 1
                    Minimum amount a value can be to match an exponential.
                    Cannot be below 1 if max_iterations is above 0 (will automatically raise to 1).
                     (eg. You could have '0.25 billion' but not '0.25 billion and 0.6 million and 2')
                    If set below 1 and there is only 1 result, the code will be rerun with max_iterations as 0.
                    Example:
                        The default is 1, so if the input was 1000 and is reduced by 1, it would switch down to hundreds.
                        If it was set to 0.1, 100 and above would display as 0.1 thousand.
                        If it was set to 10, it would move down to the previous prefix, which in this case would be 10 hundred.
                    
                    >>> LargeNumber(7654321).to_text(num_decimals=3, max_iterations=0, min_amount=1)
                    '7.654 million'
                    >>> LargeNumber(7654321).to_text(num_decimals=3, max_iterations=0, min_amount=0.001)
                    '0.008 billion'
                    >>> LargeNumber(7654321).to_text(num_decimals=3, max_iterations=0, min_amount=10)
                    '7654.321 thousand'
                    >>> LargeNumber(7654321).to_text(num_decimals=3, max_iterations=0, min_amount=10000)
                    '76543.21 hundred'
                    >>> LargeNumber(7654321).to_text(num_decimals=3, min_amount=1)
                    '7 million, 654 thousand, 3 hundred and 21'
                    >>> LargeNumber(7654321).to_text(num_decimals=3, min_amount=0.001)
                    '7 million, 654 thousand, 3 hundred and 21'
                    >>> LargeNumber(7654321).to_text(num_decimals=3, min_amount=10)
                    '7654 thousand and 321'
                    
                min_amount_limit:
                    Default: -1 (infinite)
                    How many iterations to apply min_amount to.
                    For example you may only want the min_amount to apply to the first number, and have every subsequent number
                     treated normally.
                     
                    >>> LargeNumber(7654321).to_text(num_decimals=3, min_amount=1)
                    '7 million, 654 thousand, 3 hundred and 21'
                    >>> LargeNumber(7654321).to_text(num_decimals=3, min_amount=10)
                    '7654 thousand and 321'
                    >>> LargeNumber(7654321).to_text(num_decimals=3, min_amount=10, min_amount_limit=1)
                    '7654 thousand, 3 hundred and 21'
                    >>> LargeNumber(7654321).to_text(num_decimals=3, min_amount=10, min_amount_limit=2)
                    '7654 thousand and 321'
                     
                max_iterations:
                    Default: -1 (infinite)
                    Number of separate prefixes to split the number into.
                    Set to 0 to only have a single suffix, or below 0 to display the entire number.
                    If used, the lowest prefix will have a decimal representation of the remaining number.
                     (eg. 5 hundred and 52 turns to 5.52 hundred)
                    
                    >>> LargeNumber(7654321).to_text(num_decimals=3, min_amount=1, max_iterations=-1)
                    '7 million, 654 thousand, 3 hundred and 21'
                    >>> LargeNumber(7654321).to_text(num_decimals=3, min_amount=1, max_iterations=0)
                    '7.654 million'
                    >>> LargeNumber(7654321).to_text(num_decimals=3, min_amount=1, max_iterations=1)
                    '7 million and 654.321 thousand'
                    >>> LargeNumber(7654321).to_text(num_decimals=3, min_amount=1, max_iterations=2)
                    '7 million, 654 thousand and 3.21 hundred'
                    
                use_fractions:
                    Default: False
                    Attempts to convert a decimal point into a fraction through a brute force method.
                    Will also attempt to calculate a prefix.
                    For now, it will only work if decimals is enabled, as I haven't coded in the word representations for everything.
                    Due to the precision of floating point numbers, any recurring numbers must be input as a string or calculated
                     in the Decimal format.
                    It appears to require 16 decimals, where as floating point division gives you 12.
                    
                    >>> LargeNumber(7654321.5).to_text(use_fractions=True)
                    '7 million, 654 thousand, 3 hundred and 21 and 1/2'
                    >>> LargeNumber(7654321.75).to_text(use_fractions=True)
                    '7 million, 654 thousand, 3 hundred and 21 and 3/4'
                    >>> LargeNumber(7654321.39).to_text(use_fractions=True)
                    '7 million, 654 thousand, 3 hundred and 21 and 39/100ths'
                    >>> LargeNumber(7654321.383).to_text(use_fractions=True)
                    '7 million, 654 thousand, 3 hundred and 21.383'
                    >>> LargeNumber(1.0/3.0).to_text(use_fractions=True)
                    '0.333333333333'
                    >>> LargeNumber(Decimal(1)/Decimal(3)).to_text(use_fractions=True)
                    '1/3rd'
                    >>> LargeNumber('0.333333333333333').to_text(use_fractions=True)
                    '0.333333333333333'
                    >>> LargeNumber('0.3333333333333333').to_text(use_fractions=True)
                    '1/3rd'
                    
                fraction_precision:
                    Default: 100
                    The precision of the above mentioned brute force method.
                    Determines the maximum value it will search for.
                    
                    >>> LargeNumber(7654321.39).to_text(use_fractions=True, fraction_precision=100)
                    '7 million, 654 thousand, 3 hundred and 21 and 39/100ths'
                    >>> LargeNumber(7654321.39).to_text(use_fractions=True, fraction_precision=50)
                    '7 million, 654 thousand, 3 hundred and 21.39'
                    >>> LargeNumber(7654321.393).to_text(use_fractions=True, fraction_precision=1000)
                    '7 million, 654 thousand, 3 hundred and 21 and 393/1000ths'
                    
                num_decimals:
                    Default: None (inifinite with no extra zeroes)
                    Number of decimal places to display.
                    
                    >>> import math
                    >>> LargeNumber(math.pi).to_text()
                    '3.14159265359'
                    >>> LargeNumber(math.pi).to_text(num_decimals=2)
                    '3.14'
                    >>> LargeNumber(100).to_text()
                    '1 hundred'
                    >>> LargeNumber(100).to_text(num_decimals=3)
                    '1 hundred'
                    
                force_decimals:
                    Default: False
                    If decimals should be added until the length hits num_decimals.
                    If num_decimals is set, 0's will be added to match the minimum number of decimals.
                    If num_decimals is not set, this will make sure every number is in a decimal format.
                    
                    >>> LargeNumber(100).to_text()
                    '1 hundred'
                    >>> LargeNumber(100).to_text(num_decimals=20)
                    '1 hundred'
                    >>> LargeNumber(100).to_text(force_decimals=True)
                    '1.0 hundred'
                    >>> LargeNumber(100).to_text(force_decimals=True, num_decimals=20)
                    '1.00000000000000000000 hundred'
                    >>> LargeNumber(101).to_text(force_decimals=True, max_iterations=0)
                    '1.01 hundred'
                
                min_decimals:
                    Default: 2
                    Ensures each number has a minimum amount of decimals.
                    Will not work unless force_decimals is True.
                    If num_decimals is set below min_decimals, precision will be lost.
                    
                    >>> LargeNumber(100).to_text(max_iterations=0, force_decimals=True)
                    '1.0 hundred'
                    >>> LargeNumber(100).to_text(max_iterations=0, force_decimals=True, min_decimals=3)
                    '1.000 hundred'
                    >>> LargeNumber(100.31643).to_text(max_iterations=0, force_decimals=True)
                    '1.0031643 hundred'
                    >>> LargeNumber(100.31643).to_text(max_iterations=0, force_decimals=True, min_decimals=3)
                    '1.0031643 hundred'
                    >>> LargeNumber(100).to_text(max_iterations=0, force_decimals=True, num_decimals=2, min_decimals=4)
                    '1.0000 hundred'
                    >>> LargeNumber(0.31643).to_text(force_decimals=True, num_decimals=2, min_decimals=4)
                    '0.0300'
        
        
        General Examples:
            >>> LargeNumber(100).to_text()
            '1 hundred'
            >>> LargeNumber(100).to_text(digits=False)
            'one hundred'
            >>> LargeNumber(-100).to_text()
            '-1 hundred'
            >>> LargeNumber(-100).to_text(digits=False)
            'negative one hundred'
            >>> LargeNumber(100.5).to_text()
            '1 hundred and 0.5'
            >>> LargeNumber(100.5).to_text(digits=False)
            'one hundred point five'
            >>> LargeNumber(100.5).to_text(min_amount=10)
            '100.5'
            >>> LargeNumber(100.5).to_text(min_amount=0.1)
            '0.1005 thousand'
            >>> LargeNumber(100.5).to_text(digits=False, min_amount=0.1, num_decimals=2)
            'zero point one zero thousand'
        
        Precision, Rounding and Iteration Examples:
            >>> LargeNumber(123456789.987654321).to_text()
            '123 million, 456 thousand, 7 hundred and 89.988'
            >>> LargeNumber('123456789.987654321').to_text()
            '123 million, 456 thousand, 7 hundred and 89.987654321'
            >>> LargeNumber(123456789).to_text(force_decimals=True)
            '123 million, 456 thousand, 7 hundred and 89.0'
            >>> LargeNumber(123456789).to_text(force_decimals=True, min_decimals=3)
            '123 million, 456 thousand, 7 hundred and 89.000'
            >>> LargeNumber(123456789).to_text(max_iterations=0, num_decimals=2)
            '123.46 million'
            >>> LargeNumber(123456789).to_text(max_iterations=1, num_decimals=2)
            '123 million and 456.79 thousand'
            
        Minimum Amount Examples:
            >>> input = 123456789987654321
            >>> LargeNumber(input).to_text()
            '123 quadrillion, 456 trillion, 789 billion, 987 million, 654 thousand, 3 hundred and 21'
            >>> LargeNumber(input).to_text(min_amount=1000)
            '123456 trillion, 789987 million, 6543 hundred and 21'
            >>> LargeNumber(input).to_text(min_amount=1000, min_amount_limit=1)
            '123456 trillion, 789 billion, 987 million, 654 thousand, 3 hundred and 21'
            >>> LargeNumber(input).to_text(min_amount=0.001)
            '123 quadrillion, 456 trillion, 789 billion, 987 million, 654 thousand, 3 hundred and 21'
            >>> LargeNumber(input).to_text(min_amount=0.1, max_iterations=0)
            '0.123456789987654321 quintillion'
            >>> LargeNumber(input).to_text(min_amount=1000, max_iterations=0, num_decimals=3)
            '123456.790 trillion'
        
        Fractions Examples:
            >>> LargeNumber(0.5).to_text()
            '0.5'
            >>> LargeNumber(0.5).to_text(use_fractions=True)
            '1/2'
            >>> LargeNumber(0.25).to_text(use_fractions=True)
            '1/4'
            >>> LargeNumber(0.25).to_text(use_fractions=True, fraction_precision=4)
            '1/4'
            >>> LargeNumber(0.25).to_text(use_fractions=True, fraction_precision=3)
            '0.25'
            >>> LargeNumber(0.2).to_text(use_fractions=True)
            '1/5th'
        """
        
        
        use_fractions = kwargs.get('use_fractions', False)
        fraction_precision = kwargs.get('fraction_precision', 100)
        
        num_decimals = kwargs.get('num_decimals', None)
        force_decimals = kwargs.get('force_decimals', False)
        min_decimals = kwargs.get('min_decimals', None)
        
        as_digits = kwargs.get('digits', True)
        
        num_name = []
        num_name_joined = ''
        num_output = self._calculate_number_parts(**kwargs)
        
        #Get remaining decimals for later and remove from output
        remaining_decimals = Decimal(num_output.pop(-1))
        
        #Fix for values between 0 and 1
        if not num_output:
            num_output[0] = 0
        
        #Fix to merge decimal with lowest exponential value to stop errors such as 1.000.35
        if force_decimals and remaining_decimals and num_output.get(0, 0):
            #123456789000
            only_exponential = sorted(num_output.keys())[0]
            num_output[only_exponential] = str(self._round_with_precision(str(Decimal(num_output[only_exponential])+
                                                                              Decimal(remaining_decimals)*
                                                                              Decimal('0.'+'0'*(only_exponential-1)+'1')),
                                                                          num_decimals, force_decimals))
            remaining_decimals = 0
    
        #Convert numbers to words
        sorted_keys = sorted(num_output.keys())[::-1]
        for i in sorted_keys:
            current_value = num_output[i]
            additional_value = ''
            if NumberNames.num_dict[i]:
                additional_value = ' '+NumberNames.num_dict[i]
            
            #Avoid using fractions if using prefix (eg. 0.5 billion not 1/2 billion)
            should_use_fractions = use_fractions
            if i:
                should_use_fractions = False
            
            #Add decimals only if it's the last number, and there's not remaining decimals
            if i == sorted_keys[-1] and not remaining_decimals:
                
                if force_decimals:
                    
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
                        #Stip zeroes from end of number
                        if '.' in current_value:
                            current_value = current_value.rstrip('0')
                            
                        #Only add zero if the last number is a decimal point, or also add a decimal point
                        if '.' not in current_value[:-1]:
                            if current_value[-1] != '.':
                                current_value += '.'
                            current_value += '0'
                    
                    #Pad out the decimals
                    if min_decimals:
                        num_decimal_points = len(current_value.split('.')[1])
                        if min_decimals > num_decimal_points:
                            current_value += '0'*(min_decimals-num_decimal_points)
            
            text_num = NumberNames.num_to_text(current_value, as_digits, 
                                   use_fractions=should_use_fractions, 
                                   fraction_precision=fraction_precision,
                                   print_warning=True) + additional_value
           
            
            #Fix for min_amount under 0
            if i and current_value[:10] == 'zero point':
                text_num = text_num[5:]
                
            num_name.append(text_num)
        
        #Join list
        if len(num_name)-1:
            num_name_joined += ', '.join(num_name[:-1]) + ' and '
        num_name_joined += num_name[-1]
        
        #Add decimal point
        if remaining_decimals:
            
            if not remaining_decimals:
                remaining_decimals = '0.'
                if num_decimals is not None:
                    remaining_decimals += '0'*num_decimals
                else:
                    remaining_decimals += '0'
            
            #Convert to text
            remaining_decimals = self._round_with_precision(remaining_decimals, num_decimals, force_decimals)
                            
            decimal_num = NumberNames.num_to_text(remaining_decimals, as_digits, 
                                      use_fractions=use_fractions, 
                                      fraction_precision=fraction_precision,
                                      only_return_decimal=True,
                                      print_warning=True)
            
            #Add space before 'point five'
            if not as_digits:
                decimal_num = ' '+decimal_num
            
            #Fix to stop fractions not removing a zero (eg. 0 and 2/5ths should be 2/5ths)
            if '/' in decimal_num:
                if num_name_joined and num_name_joined != '0':
                    num_name_joined += ' and '
                else:
                    num_name_joined = ''
            
            #Fix if there are no units (1 hundred.5 to 1 hundred and 0.5)
            if 0 not in num_output:
                if as_digits:
                    num_name_joined += ' and 0'
                else:
                    pass
                    #'one hundred point five' works, leaving this note here in case it needs to change
                    #num_name_joined += ' and zero'
                
            num_name_joined += decimal_num
        
        return num_name_joined
        
    def quick(self, num_decimals=3):
        """Quickly format a number with 0 iterations and 3 decimal points.
        
        Parameters:
            num_decimals:
                See LargeNumber().to_text()
        
        >>> LargeNumber('5000').quick()
        '5.000 thousand'
        >>> LargeNumber('64321764.24').quick()
        '64.322 million'
        >>> LargeNumber('-444443465400.24').quick()
        '-444.443 billion'
        """
        kwargs = {}
        kwargs['max_iterations'] = 0
        kwargs['num_decimals'] = num_decimals
        kwargs['force_decimals'] = True
        kwargs['min_decimals'] = 3
        kwargs['use_fractions'] = False
        kwargs['digits'] = True
        return self.to_text(**kwargs)
