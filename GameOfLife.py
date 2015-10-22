from collections import defaultdict
class GameOfLife(object):
    
    adjacent = ((-1,-1), (0,-1), (1,-1),
                (-1, 0),         (1, 0),
                (-1, 1), (0, 1), (1, 1))

    alive_cell = 'o'
    dead_cell = '.'
    
    def __init__(self, rule='B3/S23'):
        """Setup an empty Game Of Life object."""
        self._reset()
        self.new_rule()

    def _reset(self):
        self.game_data = {}
        self.generations = 0

    def new_rule(self, rule='B3/S23'):
        """Store the information for a new rule."""
        rules = rule.split('/')
        
        for i in range(len(rules)):
            if rules[i].lower().startswith('b'):
                self.rule_born = map(int, list(rules[i][1:]))
                
            elif rules[i].lower().startswith('s'):
                self.rule_alive = map(int, list(rules[i][1:]))
    
    def paste(self, cells, offset=(0, 0), clear=False):
        """Paste a string to act as cells.

        Use 'o' to bring a cell to live, and '.' to kill a cell.
        An empty space will not modify the cell under it.
        """
        if clear:
            self._reset()
            
        y = None
        for line in cells.splitlines():

            #Ignore any initial empty lives
            if y is not None:
                y += 1
            elif line and y is None:
                y = 0

            for x in range(len(line)):
                if line[x] == self.alive_cell:
                    self.add((x + offset[0], y + offset[1]))
                elif line[x] == self.dead_cell:
                    self.remove((x + offset[0], y + offset[1]))
                    
            
    def add(self, coordinate):
        """Add a cell."""

        #Add to dictionary
        if coordinate[1] not in self.game_data:
            self.game_data[coordinate[1]] = set([coordinate[0]])
            
        elif coordinate[0] not in self.game_data[coordinate[1]]:
            self.game_data[coordinate[1]].add(coordinate[0])
    

    def remove(self, coordinate):
        """Delete a cell.""" 

        #Remove point from dictionary
        if (coordinate[1] in self.game_data
            and coordinate[0] in self.game_data[coordinate[1]]):
            self.game_data[coordinate[1]].remove(coordinate[0])

            #Delete column if no more values
            if not self.game_data[coordinate[1]]:
                del self.game_data[coordinate[1]]
        

    def find_all_adjacent(self):
        """Find the number of adjacent cells to each cell.

        It will build a list of all the cells currently alive or
        touching something alive, then iterate through each one to
        find how many they are touching.
        """
        all_coordinates = set()
        adjacent_amount = {}

        #Iterate through dictionary to build list of all cells
        for y in self.game_data:
            for x in self.game_data[y]:
                num_adjacent = 0
                
                for i in self.adjacent:
                    c = (x + i[0], y + i[1])
                    if (c[1] in self.game_data
                        and c[0] in self.game_data[c[1]]):
                        num_adjacent += 1
                        
                    all_coordinates.add(c)
                adjacent_amount[(x, y)] = num_adjacent

        #Find neighbours for each cell
        for coordinate in all_coordinates:
            if coordinate not in adjacent_amount:
                num_adjacent = 0
                
                for i in self.adjacent:
                    c = (coordinate[0] + i[0],
                         coordinate[1] + i[1])
                    if (c[1] in self.game_data
                        and c[0] in self.game_data[c[1]]):
                        num_adjacent += 1
                        
                adjacent_amount[coordinate] = num_adjacent
                
        return adjacent_amount
    
    def step(self, n=1):
        """Move forward n steps in the generation."""
        
        for i in range(n):
            
            self.generations += 1
            adjacent_blocks = self.find_all_adjacent()
            
            for cell in adjacent_blocks:
                neighbours = adjacent_blocks[cell]
                alive = (cell[1] in self.game_data
                         and cell[0] in self.game_data[cell[1]])
                
                if (not alive and neighbours in self.rule_born
                    or alive and neighbours in self.rule_alive):
                    self.add(cell)
                else:
                    self.remove(cell)
    
    
    def __str__(self):
        """Print the current state of the cells."""

        output = []
        min_x = '' #String so it will always be larger than a number
        
        #Fix for if game_data is empty
        if not self.game_data:
            y_range = ()
        else:
            y_range = range(min(self.game_data), max(self.game_data) + 1)
            
            #Find lowest X value to offset the printing by
            for y in y_range:
                if y in self.game_data:
                    min_x_value = min(self.game_data[y])
                    if min_x_value < min_x:
                        min_x = min_x_value
            
        #Generate each cell a line at a time
        for y in y_range:
            last_x = min_x
            
            if y in self.game_data:
                x_list = sorted(self.game_data[y])
            else:
                x_list = []
            
            output_text = ''
            for x in x_list:
                output_text += ' ' * max(0, 2 * (x - last_x) + 1) + 'o'
                last_x = x + 1
            output.append(output_text)
            
        return '\r\n'.join(output)
