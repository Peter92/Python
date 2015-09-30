import os
import time
import string
import sys
import cPickle
from collections import defaultdict

class RecursiveDict(object):
    """Class for making it easier to edit dictionaries
    containing other dictionaries in a recursive structure.
    """
    def __init__(self, input_dict):
        """Pass in the dictionary to use.
        
        Parameters:
            input_dict (dict): Dictionary to use.
        """
        self.input_dict = input_dict
        
    def write(self, path, value=None, overwrite=True, overwrite_end=True):
        """Write to a dictionary recursively using a list.
        
        Will return True if successful or False if not.
        
        Parameters:
            path (list): A list containing the structure on how
                to get to the value.
            
            value (any or None): The value to write to the end of 
                the dictionary. If None, the value will be taken 
                as the last value from the path.
                Defualt: None
            
            overwrite (bool): If overwriting other values such
                as strings is allowed when building the structure.
                Defualt: True
            
            overwrite_end (bool): If overwriting the final value
                is allowed if it exists. Will automatically set
                to True if overwrite is also True.
                Defualt: True
        """
        if overwrite:
            overwrite_end = True
            
        #Get value from last item in path if not provided
        if value is None:
            value = path[-1]
            path = path[:-1]
        path_len = len(path)-1
        
        reduced_dictionary = self.input_dict
        
        #Build the path (or check it's not overwriting anything)
        for i in range(path_len):
            
            key = path[i]
            
            if reduced_dictionary.get(key, None) is None:
                reduced_dictionary[key] = {}
            
            if not isinstance(reduced_dictionary[key], dict):
                if overwrite:
                    reduced_dictionary[key] = {}
                else:
                    return False
                
            if i < path_len:
                reduced_dictionary = reduced_dictionary[key]
        
        #Write value
        if (isinstance(reduced_dictionary, dict) and reduced_dictionary.get(path[-1], {}) == {}) or overwrite_end:
            reduced_dictionary[path[-1]] = value
            return True
        return False

        
    def get(self, path):
        """Get the values contained in a recursive structure.
        Uses the reduce function but just makes it more conveniant.
        
        Parameters:
            path (list): A list containing the structure on how
                to get to the value.
        """
        return reduce(dict.__getitem__, path, self.input_dict)
        
def split_list(x, n):
    """Split a list by n characters."""
    n = int(n)
    if n:
        return [x[i:i+n] for i in range(0, len(x), n)]
    else:
        return ['' for i in x]
    
def flatten_list(x):
    """Convert nested lists into one single list."""
    return [j for i in x for j in i]
              
def get_max_dict_keys(x):
    """Return a list of every key containing the max value.
    
    Parameters:
        x (dict): Dictionary to sort and get highest value.
            It must be a dictionary of integers to work properly.
    """
    if x:
        sorted_dict = sorted(x.iteritems(), key=operator.itemgetter(1), reverse=True)
        if sorted_dict[0][1]:
            return sorted([k for k, v in x.iteritems() if v == sorted_dict[0][1]])
    return []

def join_words(x):
    return ''.join(ucfirst(i) for i in str(x).strip().split())

def ucfirst(x):
    x = str(x)
    return x[0].upper() + x[1:]

def list_to_text(value, connector='', comma=',', last_comma=False):
    """Convert a list into a readable format.
    If 'to' or '-' is given as a connector, only the first and last list values will be used.
    
    >>> list_to_text([0,1,2,3,4,5])
    '0, 1, 2, 3, 4, 5'
    >>> list_to_text([0,1,2,3,4,5], 'and')
    '0, 1, 2, 3, 4 and 5'
    >>> list_to_text([0,1,2,3,4,5], 'to')
    '0 to 5'
    >>> list_to_text([0,1,2,3,4,5], '-')
    '0-5'
    >>> list_to_text([2])
    '2'
    """
    
    value = [str(i) for i in value]
    if len(value) == 1:
        return value[0]
    elif value:
        if connector:
            if connector in ('to', '-'):
                if connector == 'to':
                    connector = ' to '
                return value[0] + connector + value[-1]
            return (comma+' ').join(value[:len(value)-1]) + ' ' + connector + ' ' + value[-1]
        else:
            return (comma+' ').join(value)
    return ''

class TimeThis(object):
    """Class that can be used to output the time taken. It may be
    used with the 'with' command, which will time everything within
    the indent.
    
    Example:
        import time, random
        with TimeThis() as t:
            time.sleep(0.47)
            print 'Sleep 1: {}'.format(t.output())
            time.sleep(0.91)
            print 'Sleep 2: {}'.format(t.output())
            time.sleep(1.234)
    
        Sleep 1: 0.47 seconds
        Sleep 2: 1.38 seconds
        Total time taken: 2.62 seconds
    """
    def __init__(self, current_time=None, print_time=True):
        """Pass in a custom time if needed.
        
        Parameters:
            current_time (int, float or None, optional): Input a custom
                time to use instead.
            
            print_time (bool): If the total time should be printed
                at the end of the execution.
        """
        self.current_time = current_time
        self.print_time = print_time

    def __enter__(self):
        """Executed when TimeThis is used with the 'with' command."""
        self.st = self.current_time or time.time()
        return self
        
    def __exit__(self, *args):
        """Executed after TimeThis has been used with the 'with' command.
        Three values are passed in but don't seem to relate to anything.
        """
        if self.print_time:
            print "Total time taken: {}".format(self.output())
    
    def current(self):
        """Return float of time taken."""
        try:
            return time.time() - self.st
        except AttributeError:
            return 0.0
    
    def output(self, auto=True, accuracy=2, decimals=None, 
               years=True, days=True, hours=True, minutes=True, seconds=True):
        """Return a formatted version of the time taken.
        
        Parameters:
            days (bool): If returning number of days is allowed.
            
            hours (bool): If returning number of hours is allowed.
            
            minutes (bool): If returning number of minutes is allowed.
            
            seconds (bool): If returning number of seconds is allowed.
            
            auto (bool): If the returned values should be limited in length.
                For example, if something takes 3 days, you don't need to
                know to the nearest second.
            
            accuracy (int): Maximum number of values to return with the
                auto setting.
            
            decimals (int or None): Number of decimals to show on the last
                value. leave as None to show up to 2 decimals for each
                number, or 3 if the number is below 1.
        
        Tests:
            >>> t = TimeThis(123456789.987654321)
            >>> t.output()
            3 years and 333.17 days
            >>> t.output(years=False, days=False, hours=False)
            2057613 minutes and 9.99 seconds
            >>> t.output(accuracy=3)
            3 years, 333 days and 4.11 hours
            >>> t.output(decimals=0)
            3 years and 333 days
            >>> t.output(auto=False, days=False)
            3 years, 7996 hours, 6 minutes and 51.99 seconds
        """
        
        
        if self.current_time is not None:
            current_time = float(self.current_time)
        else:
            current_time = self.current()
        
        accuracy = int(max(1, accuracy))
        current_time = max(current_time, -current_time)
        num_decimals = decimals
        
        start = None
        output_number = []
        output_text = []
        all_times = []
        all_names = []
        
        #Calculate time
        if years:
            num_years = current_time / 31556926
            current_time -= int(num_years) * 31556926
            all_times.append(num_years)
            all_names.append('year')
        if days:
            num_days = current_time / 86400
            current_time -= int(num_days) * 86400
            all_times.append(num_days)
            all_names.append('day')
        if hours:
            num_hours = current_time / 3600
            current_time -= int(num_hours) * 3600
            all_times.append(num_hours)
            all_names.append('hour')
        if minutes:
            num_minutes = current_time / 60
            current_time -= int(num_minutes) * 60
            all_times.append(num_minutes)
            all_names.append('minute')
        if seconds or not all_times:
            all_times.append(current_time)
            all_names.append('second')
        
        
        #Build list of values, limited by accuracy if auto is True
        for i in range(len(all_times)):
            if auto and len(output_number) > accuracy-1:
                break
            if output_number or int(all_times[i]):
                output_number.append(all_times[i])
                output_text.append(all_names[i])
        
        #Fix for if time is less than 1 second
        if not output_number:
            output_number.append(all_times[-1])
            output_text.append(all_names[-1])
            if num_decimals is None:
                decimals = 3
        if num_decimals is None:
            decimals = 2
        
        #Format the numbers so that only the last number has decimals
        final_number = str(round(output_number[-1], decimals)).split('.')
        output_number = [int(i) for i in output_number[:-1]] + [final_number[0]]
        if decimals:
            use_decimals = num_decimals is not None or self.current_time is None
            output_number[-1] += '.' + final_number[1].ljust(decimals if use_decimals else 0, '0')
            
        #Join the text and numbers together
        output = ['{} {}{}'.format(output_number[i], output_text[i], 's' if str(output_number[i]) != '1' else '') for i in range(len(output_number))]
                
        return list_to_text(output, 'and')

        
def make_file_path(path):
    path_split = [i[::-1] for i in path.replace('\\\\', '\\').replace('\\', '/')[::-1].split('/', 1)]
    folder_path = path_split[1]
    if '.' not in path_split[0]:
        folder_path += '/' + path_split[0]
    try:
        os.makedirs(folder_path + '/')
    except WindowsError:
        pass
    return os.access(folder_path, os.W_OK)
    

class NewConfigParser(object):
    """Read or write to a config file.
    This was mainly coded as an alternative to ConfigParser, as it was
    causing too many problems for something relatively simple.
    
    Main Parameters:
        section (str): The headers in the config file to group the
            options. 
            
        option (str): The name of each value.
        
        value (str, bool, float, int, None): Value to store.
    
    Example config.ini:
        [Section1]
        Option1 = Value1
        Option2 = Value2
        
        [Section2]
        Option1 = Value3
    
    Instead of the functions such as .getfloat(), the option name will
    be modified if the value is boolean, integer or float. This is case
    sensitive, and relies on the option names to be capitalised, with
    the first letter being lowercase if the input is not a string.
    This is done automatically by the code, just be careful when
    manually editing the file.
    
    For example:
        some int = 42 will change to 'iSomeInt = 42'
        some int = '42' will change to 'SomeInt = 42'
        
    If a comment is used, the above will only apply if a value is also
    given. This is because a line may only be temporarily commented out,
    so may still need the stored value at a later date.
    
        ;a comment will stay as ';a comment'
        ;a comment = 42 will change to ';iAComment = 42'
    
    If there is no value, it will be used as None.
        TextOption will be read as {'TextOption': None}
        TextOption = None will be wrote as 'TextOption'
    """
    
    allowed_types = (unicode, str, bool, float, int, type(None))
    prefixes = {'b': bool,
                'f': float,
                'i': int}
    comment_markers = (';', '!')
    
    def __init__(self, config_filename):
        self.config_filename = config_filename
        self.refresh()

    def refresh(self):
        """Read all values from config file.
        This is done once each time NewConfigParser is used, to avoid
        having to read the file each time the user needs a single value.
        """
        try:
            with open(self.config_filename, 'r') as f:
                config_contents = f.read().splitlines()
        except IOError:
            config_contents = None
        
        self.config_data = defaultdict(dict)
        current_section = None
        if config_contents:
            for i in config_contents:
                
                #Skip empty lines
                if not i:
                    continue
                    
                #Mark new section
                if i[0] == '[' and i[-1] == ']':
                    current_section = i[1:-1]
                else:
                    if current_section is None:
                        print 'error'
                        break
                    else:
                        if '=' in i:
                            
                            #Get if comment then treat like a normal value
                            comment_marker = ''
                            if any(i.startswith(j) 
                                   for j in self.comment_markers):
                                comment_marker = i[0]
                                i = i[1:]
                            
                            option_split = (j.strip() for j in i.split('=', 1))
                            option, value = option_split
                            
                            #Convert value to correct type
                            value_type = self.prefixes.get(option[0], str)
                            
                            #Fix to work with boolean values, since
                            # bool('False') == True
                            if value_type == bool:
                                value = value.lower() not in ('false', '0')
                            else:
                                value = value_type(value)
                            
                            option = comment_marker + option
                            
                        else:
                            option = i.strip()
                            value = None
                            
                        self.config_data[current_section].update({option: value})
            
            #Convert back to normal dict
            self.config_data = dict(self.config_data)
            self.original_config_data = dict(self.config_data)
    
    def get_sections(self):
        """Returns a list of section names."""
        return self.config_data.keys()
    
    def get_options(self, section):
        """Returns a list of option names for the section."""
        try:
            return self.config_data[section].keys()
        except KeyError:
            raise ConfigParserError("config section not in file")
    
    def get_value(self, section, option):
        """Returns the value of an option.
        Basically this uses read(), it's just here to follow on from
        get_sections() and get_options().
        """
        if section is None:
            raise ConfigParserError("config section not in file")
        if option is None:
            raise ConfigParserError("config option not in file")
        return self.read(section, option)
    
    def read(self, section=None, option=None):
        """Read data from the config.
        If section or option is left as None, all of them will be read.
        If it is unable to find the section or option, an error will be
        raised.
        """
        if section is not None:
            try:
                section_data = self.config_data[section]
            except KeyError:
                raise ConfigParserError("config section not in file")
                
            if option is not None:
                try:
                    return self.config_data[section][option]
                except KeyError:
                    raise ConfigParserError("config option not in file")
                    
            return section_data
        return self.config_data
    
    def _rewrite_file(self, remove_comments=False):
        """Convert the dictionary of values into a list and write to the
        file.
        A backup file will also be written and deleted, so in the case
        of an error it can be recovered.
        
        Parameters:
            remove_comments (bool): If comments should be ignored when
                writing the file. Note that this cannot be undone and
                all existing comments will be wiped.
        """
        
        backup_filename = '{}.tmp'.format(self.config_filename)
        
        #Build flat list with all the values
        config_file_list = []
        for section in self.config_data:
            if config_file_list:
                config_file_list.append('')
            config_file_list.append('[{}]'.format(section))
            
            for option in self.config_data[section]:
                value = self.config_data[section][option]
                if value is not None:
                    option += ' = {}'.format(value)
                config_file_list.append(option)
        
        if remove_comments:
            config_file_list = [i for i in config_file_list 
                                if not any(i.startswith(j) 
                                for j in self.comment_markers)]
        
        file_data = '\r\n'.join(config_file_list)
        
        #Make copy of backup file if it exists
        if os.path.isfile(backup_filename):
            old_config = NewConfigParser(backup_filename).config_data
            current_config = NewConfigParser(self.config_filename).config_data
            new_backup_name = '{}.{}.old'.format(self.config_filename,
                                                 int(time.time()))
            if old_config != current_config:
                
                with open(new_backup_name, 'w') as f:
                    f.write(file_data)
        
                print ('Temporary file exists and contains different data, '
                       "saved it as '{}'.").format(new_backup_name)
        
        #Write to backup file
        with open(backup_filename, 'w') as f:
            f.write(file_data)
        
        #Overwrite main file 
        with open(self.config_filename, 'w') as f:
            f.write(file_data)
        
        #Delete backup file
        os.remove(backup_filename)
        
        
    def write(self, data, update_values, write_values, 
              remove_comments=False):
        """Write the required input to a config file.
        A dictionary containing all values (including ones not written
        because of write_values) will be returned.
        
        Parameters:
            data (dict): Dictionary storing the values to write to the
                config. The keys are the section names, and values
                should store another dictionary of the corresponding
                option names and values.
                Example: data = {'Section1': {'Option1': 'Value1',
                                              'Option2': 'Value2'},
                                 'Section2': {'Option1': 'Value3'}}
            
            update_values (bool): If existing values should be updated
                with the new value.
            
            write_values (bool): If non existing values should be added
                to the dictionary.
            
            remove_comments (bool): See NewConfigParser._rewrite_file()
        """
        #Check all values are the correct type
        if not all(all(type(i) in self.allowed_types for i in v.values()) 
                   for k, v in data.iteritems()):
            raise ConfigParserError("invalid value type")
          
        reversed_prefix = {v: k for k, v in self.prefixes.iteritems()}
        
        all_data = defaultdict(dict)
        original_config_data = cPickle.dumps(self.config_data.copy())
        
        for section in data:
            
            #Add section if it doesn't exist
            if section not in self.config_data:
                if write_values:
                    self.config_data[section] = {}
                else:
                    print 'not found'
                    continue
            
            #Write or update values
            for option in data[section]:
                
                value = data[section][option]
                
                #Format option name to contain value type
                option_no_prefix = option
                if value is not None:
                    
                    comment_marker = ''
                    if any(option.startswith(i) for i in self.comment_markers):
                        comment_marker = option[0]
                        option = option[1:]
                    
                    option = join_words(option)
                    option_no_prefix = option
                
                    value_type = type(value)
                    if value_type in reversed_prefix:
                        option = reversed_prefix[value_type] + option
                    
                    option = comment_marker + option
                

                #Update value
                if option in self.config_data[section]:
                    if update_values:
                        self.config_data[section][option] = value
                    stored_value = self.config_data[section][option]
                    all_data[section][option_no_prefix] = stored_value
                
                #Write value
                else:
                    all_data[section][option_no_prefix] = value
                    if write_values:
                        self.config_data[section][option] = value
        
        #Only rewrite file if needed
        changed_data = original_config_data != cPickle.dumps(self.config_data)
        #if update_values or write_values or remove_comments:
        if changed_data or remove_comments:
            self._rewrite_file(remove_comments)
        
        self.refresh()
        return dict(all_data)
