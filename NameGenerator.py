from __future__ import division
from string import ascii_lowercase, ascii_uppercase
import random

def quick_round(i):
    if i % 1 >= 0.5:
        i += 1
    return int(i)


class WordGenerator(object):
    def __init__(self, bank_size):
        self.size = bank_size
        self.cache = {}
    
    def build(self, file_name, custom_name, line_end='\r\n', depth=2):
        with open(file_name) as f:
            contents = f.read()
            file_hash = self._find_hash(contents)
        
        rebuild_invalid = custom_name if custom_name in self.cache else None
        if custom_name not in self.cache:
            hashes = {v['Hash']: k for k, v in self.cache.iteritems()}
            
            #Reference existing value
            if file_hash in hashes:
                self.cache[custom_name] = {'Alias': hashes[file_hash],
                                           'Hash': None,
                                           'Words': None,
                                           'WordBank': None,
                                           'Invalid': None}
                rebuild_invalid = hashes[file_hash]
                    
            #Create new values
            else:
                words = [i for i in contents.lower().split(line_end) if i]
                self.cache[custom_name] = {'Alias': None,
                                           'Hash': file_hash,
                                           'Words': words,
                                           'WordBank': self._build_dictionary(words),
                                           'Invalid': {depth: self._build_invalid(words, depth)}}
                rebuild_invalid = custom_name
        
        #Create new invalid depth if the requested one isn't already in the cache
        if rebuild_invalid:
            if depth not in self.cache[rebuild_invalid]['Invalid']:
                self.cache[rebuild_invalid]['Invalid'][depth] = self._build_invalid(self.cache[rebuild_invalid]['Words'], depth)

    def _find_hash(self, data):
        """Leaving this here with a potential for a better hash."""
        return hash(data)

    def _build_dictionary(self, words):
        
        bank = [{} for _ in xrange(self.size)] + [{}, 0]
        
        for word in words:
            
            word_len = len(word)
            index_start = 0
            bank[-1] += 1
            
            try:
                bank[-2][word_len] += 1
            except KeyError:
                bank[-2][word_len] = 1
            
            for i, character in enumerate(word):
                
                #Generate the start and end index for the bank
                index_end = quick_round(((i + 1) / word_len) * (self.size - 1))
                
                #Write to the bank
                for n in xrange(index_start, index_end + 1):
                    try:
                        bank[n][character] += 1
                    except KeyError:
                        try:
                            bank[n][character] = 1
                        except KeyError:
                            bank[n] = {character: 1}
                
                index_start = index_end + 1
        return bank

    def _build_invalid(self, words, max_depth, _current_phrase='', _invalid=None, _current_depth=1):
        results = set()
        for letter in ascii_lowercase:
            new_phrase = _current_phrase + letter
            found = False
            for word in words:
                if new_phrase in word:
                    found = True
                    break
            if found and _current_depth < max_depth:
                results.update(self._build_invalid(words, max_depth, _current_phrase=new_phrase, _invalid=_invalid, _current_depth=_current_depth + 1))
            if not found and new_phrase:
                results.add(new_phrase)
        return results
        
    def _generate_length(self, group_name, rnd=None):
        
        if rnd is None:
            rnd = random
        
        bank = self.cache[group_name]['WordBank']
        #word_index = QuickRandom().range(1, bank[-1]) - 1
        word_index = rnd.randrange(0, bank[-1])
        total = 0
        for i in sorted(bank[-2].keys()):
            total += bank[-2][i]
            if total > word_index:
                return i
        raise ValueError('no word length found')


    def generate_word(self, group_name, custom_word=None, seed=None, depth=2, max_retries=5):
        
        #Make random seed
        current_seed = []
        if custom_word is not None:
            current_seed.append(custom_word)
        if seed is not None:
            current_seed.append(seed)
        if current_seed:
            rnd = random.Random(''.join(map(str, current_seed)))
        else:
            rnd = random
        
        if group_name not in self.cache:
            raise ValueError('group {} doesn\'t exist'.format(group_name))
        
        if self.cache[group_name]['Alias'] is not None:
            group_name = self.cache[group_name]['Alias']
        bank = self.cache[group_name]['WordBank']
        if depth not in self.cache[group_name]['Invalid']:
            self.cache[group_name]['Invalid'][depth] = self._build_invalid(self.cache[group_name]['Words'], depth)
        
        size = self._generate_length(group_name, rnd)
        if custom_word is not None:
            word_size = len(custom_word)
            size += word_size
            size //= 2
    
        word_generation = ''
        index_start = 0
        for i in range(size):
            index_end = quick_round(((i + 1) / size) * (self.size - 1))
            
            retries = 0
            
            while True:
                
                #Pick index of letter
                num_letters = bank[-1] * (index_end - index_start + 1)
                #letter_required = QuickRandom().range(0, num_letters)
                letter_required = rnd.randint(0, num_letters)
                
                #Find that letter
                index_offset = max(0, letter_required - 1)
                letter_required -= index_offset // bank[-1] * bank[-1]
                index_current = index_start + index_offset // bank[-1]
                
                count = 0
                for j in ascii_lowercase:
                    try:
                        if not bank[index_current][j]:
                            raise KeyError()
                    except KeyError:
                        pass
                    else:
                        count += bank[index_current][j]
                        if count >= letter_required:
                            break
                potential_new_word = word_generation + j
                
                #Check if any parts of the word are invalid
                invalid = False
                for j in range(len(potential_new_word)):
                    if potential_new_word[-j:] in self.cache[group_name]['Invalid']:
                        invalid = True
                        
                if not invalid:
                    word_generation = potential_new_word
                    break
                    
                if retries > max_retries:
                    #print 'Failed to generate word, {} was not valid'.format(potential_new_word)
                    if custom_word is None:
                        custom_word = potential_new_word
                    return self.generate_word(group_name, custom_word=custom_word + '0', seed=seed, depth=depth, max_retries=max_retries)
                retries += 1
            
            index_start = index_end + 1
        
        return word_generation
    
    def generate_name(self, *args):
        return ' '.join(self.generate_word(i).capitalize() for i in args)
    
    def generate_sentence(self, group_name, sentence, seed=None):
        result = []
        for paragraph in (i.strip() for i in sentence.strip().replace('\r\n', '\r').replace('\n', '\r').split('\r')):
            current_paragraph = []
            for single_sentence in (i.strip() for i in paragraph.split('.')):
                current_sentence = []
                for phrase in (i.strip() for i in single_sentence.split(',')):
                    current_phrase = []
                    for word in phrase.split():
                        if word[0] in ascii_uppercase and current_phrase:
                            current_word = [word]
                        else:
                            current_word = []
                            for split_word in word.split('-'):
                                current_word.append(self.generate_word(group_name, custom_word=split_word, seed=seed))
                        current_phrase.append('-'.join(current_word))
                    current_sentence.append(' '.join(current_phrase))
                    
                current_sentence[0] = current_sentence[0][:1].capitalize() + current_sentence[0][1:]
                current_paragraph.append(', '.join(current_sentence))
            result.append('. '.join(current_paragraph))
        return '\r\n'.join(result)
try:
    old_cache = a.cache
except NameError:
    word_gen = WordGenerator(40)
else:
    word_gen = WordGenerator(40)
    word_gen.cache = old_cache
    
word_gen.build('C:/code/CSV_Database_of_First_Names.csv', 'names_en_first', depth=3)
word_gen.build('C:/code/CSV_Database_of_Last_Names.csv', 'names_en_last')

for i in range(10):
    print word_gen.generate_name('names_en_first', 'names_en_last')
