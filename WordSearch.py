import random

grid_size = 20
num_iterations = 100
second_pass = True
fill_empty_values = True
capitalize_non_matches = True

difficulty_level = 5
'''Difficulty levels:
    0: Right
    1: Right, down
    2: Right, down, with right-down dragonal
    3: Right, down, up, with right diagonals
    4: All directions, with right diagonals
    5: All directions, with all diagonals
'''
with open('C:/Code/wordsEn.txt') as f:
    word_list = f.read().split('\r\n')
input_words = [i for i in word_list if 3<len(i)<grid_size]
    
grid_directions = [0, 1, 2, 3, 4, 5, 6, 7]

grid_directions = [0]
if difficulty_level > 0:
    grid_directions.append(2)
if difficulty_level > 1:
    grid_directions.append(1)
if difficulty_level > 2:
    grid_directions += [6, 7]
if difficulty_level > 3:
    grid_directions.append(4)
if difficulty_level > 4:
    grid_directions += [3, 5]


count = 0
max_len = len(str(grid_size**2-1))
for i in range(grid_size):
    print ' '.join(str(i+count).zfill(max_len) for i in range(grid_size))
    count += grid_size
    

def convert_coordinate(grid_size, index=0):
    """Convert a number into its coordinate.
    
    >>> convert_coordinate(10, 57)
    (5, 7)
    """
    return (index/grid_size, index%grid_size)

def direction_text(direction):
    return ('right', 'down-right', 'down', 'down-left', 'left', 'left-up', 'up', 'right-up')[direction]

def direction_coordinate(grid_size, inital_location, direction):
    """Calculate the new coordinate based on a direction.
    0 = right
    1 = diagonal right-down
    2 = down
    3 = diagonal left-down
    4 = left
    5 = diagonal left-up
    6 = up
    7 = diagonal right-up
    
    >>> direction_coordinate(10, 57, 6)
    (4, 7)
    """
    directions = {}
    directions['right'] = 1
    directions['down'] = grid_size
    directions['left'] = -directions['right']
    directions['up'] = -directions['down']
    
    direction_move = (directions['right'],
                      directions['right']+directions['down'],
                      directions['down'],
                      directions['left']+directions['down'],
                      directions['left'],
                      directions['left']+directions['up'],
                      directions['up'],
                      directions['right']+directions['up'],
    )
    old_coordinate = convert_coordinate(grid_size, inital_location)
    new_location = inital_location+direction_move[direction]
    new_coordinate = convert_coordinate(grid_size, new_location)
    
    if all(new_coordinate[i] in (old_coordinate[i]+j for j in xrange(-1, 2)) for i in xrange(2)) and grid_size <= new_location < grid_size**2:
        return new_location

def word_variations(used_words, min_length=1):
    
    word_list = []
    while len(word_list) < min_length:
        for word in used_words.keys():
            word_len = len(word)
            word_range = xrange(word_len)
            
            for repeat in xrange(random.randint(0, 4)):
                
                #Remove random letters from the word - word = wrd, wod, etc
                remove_letters = random.sample(word_range, random.randint(0, word_len/3))
                num_removed_letters = 0
                for index in remove_letters:
                    word = word[:index-num_removed_letters]+word[index+1-num_removed_letters:]
                    num_removed_letters += 1
                
                #Replace random letters in word - word = ward, wore, wond, etc
                word_section = sorted(random.sample(word_range, 2))
                if word_section[0] or word_section[1] != word_len or True:
                    
                    new_word = word[random.randint(0, word_section[0]):random.randint(word_section[1], word_len)]
                    new_word_len = len(new_word)
                    
                    for replacement in xrange(random.randint(0, new_word_len/2)):
                        replacement_index = random.randint(0, new_word_len-1)
                        new_letter = random.choice(all_letters)
                        new_word = new_word[:replacement_index]+new_letter+new_word[replacement_index+1:]
    
                        word_list.append(new_word)
    return word_list
    

grid_keys = range(grid_size**2)
grid_data = [['', False] for i in grid_keys]
used_words = {}

#Stage 1 = add word
#Stage 2 = add 0-2 incorrect word copy
all_letters = ''.join(word_list)
for stage in xrange(1+second_pass):
    
    if stage:
        word_list = word_variations(used_words, num_iterations)
    else:
        word_list = input_words
                    
    for i in range(num_iterations):
        
        #Cancel loop when out of words
        if not word_list and not stage:
            break
        
        #print "Starting coordinate:", current_coordinate, convert_coordinate(grid_size, current_coordinate)
        
        random.shuffle(grid_directions)
        
        max_iters = 0
        initial_word_list = []
        
        #Build list of matching words
        if word_list:
            while not initial_word_list:
                
                #Temporary to make sure no errors
                max_iters += 1
                if max_iters > 100:
                    print 4254
                    break
            
                current_coordinate = random.choice(grid_keys)
                using_new_letter = False
                if not grid_data[current_coordinate][0]:
                    grid_data[current_coordinate][0] = random.choice(word_list)[0]
                    using_new_letter = True
                
                #Create a selection of words
                initial_word_list = [word for word in word_list if grid_data[current_coordinate][0] in word[0]]
                #initial_word_list = random.sample(initial_word_list, min(len(initial_word_list), num_iterations))
                
        else:
            initial_word_list = []
        
        valid_word = None
        
        if initial_word_list:
            for direction_index in xrange(len(grid_directions)):
                
                direction = grid_directions[direction_index]
                
                next_direction = current_coordinate
                matching_word_list = initial_word_list
                random.shuffle(matching_word_list)
                
                
                #Loop while there are matching words
                count = 0
                while matching_word_list:
                    
                    
                    #Cancel if invalid direction
                    if next_direction is None:
                        matching_word_list = []
                        break
                    
                    #Loop for each word
                    invalid_word_index = []
                    delete_count = 0
                    for i in xrange(len(matching_word_list)):
                        
                        i -= delete_count
                        
                        #Add to invalid words if the letter doesn't match
                        if grid_data[next_direction][0] and grid_data[next_direction][0] != matching_word_list[i][count]:
                            del matching_word_list[i]
                            delete_count += 1
                            
                            if not matching_word_list:
                                break
                            
                        #If reached the length of a word, it's succeeded
                        elif count >= len(matching_word_list[i])-1:
                            
                            #Choose whether to stop here or continue for a longer word
                            if random.uniform(0, 1) < 1.0/(max(1, len(matching_word_list)/2)):
                                valid_word = matching_word_list[i]
                                matching_word_list = []
                                break
                            else:
                                del matching_word_list[i]
                                delete_count += 1
                    
                    next_direction = direction_coordinate(grid_size, next_direction, direction)
                    count += 1
                
                
                #Update the grid data
                if valid_word is not None:
                    
                    if not stage:
                        used_words[word_list.pop(word_list.index(valid_word))] = (current_coordinate, direction)
                        grid_data[current_coordinate][1] = True
                    
                    next_direction = current_coordinate
                    for i in range(1, len(valid_word)):
                        
                        letter = valid_word[i]
                        next_direction = direction_coordinate(grid_size, next_direction, direction)
                        if not grid_data[next_direction][0]:
                            grid_data[next_direction][0] = letter
                            
                        #If the data doesn't match the word, this shouldn't happen
                        elif grid_data[next_direction][0] != letter:
                            grid_data[next_direction][0] = 'error'
                        
                        #Capitalise all other values
                        if not stage and capitalize_non_matches:
                            grid_data[next_direction][1] = True
                            
                        
                    break
                
                #Remove single remaining letters if the word was not completed
                elif len(grid_directions)-1 == direction_index:
                    if using_new_letter:
                        grid_data[current_coordinate][0] = ''
                        grid_data[current_coordinate][1] = False

alphabet = 'abcdefghijklmnopqrstuvwxyz'
if fill_empty_values:
    for i in xrange(len(grid_data)):
        if not grid_data[i][0]:
            grid_data[i][0] = random.choice(alphabet)
    

print ', '.join(sorted(used_words.keys()))

count = 0
for i in xrange(grid_size):
    current_row = []
    for j in xrange(grid_size):
        letter = grid_data[count][0]
        if not letter:
            letter = ' '
        if not grid_data[count][1]:
            letter = letter.upper()
        current_row.append(letter)
        count += 1
    print ' '.join(current_row)
    
