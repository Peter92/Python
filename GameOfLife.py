from collections import defaultdict

class GameOfLife(object):
    
    adjacent = ((-1,-1), (0,-1), (1,-1),
                (-1, 0),         (1, 0),
                (-1, 1), (0, 1), (1, 1))
    
    def __init__(self):
        self.game_data = defaultdict(int)
        self.store_data = dict()
        self.generations = 0
    
    def add(self, coordinate):
        if coordinate[1] not in self.game_data:
            self.game_data[coordinate[1]] = set()
            
        if coordinate[0] not in self.game_data[coordinate[1]]:
            self.game_data[coordinate[1]].add(coordinate[0])
           
        if 'lowest_x_val' not in self.store_data or coordinate[0] < self.store_data['lowest_x_val']:
            self.store_data['lowest_x_val'] = coordinate[0]
                

    def remove(self, coordinate):
        if coordinate[1] in self.game_data and coordinate[0] in self.game_data[coordinate[1]]:
            self.game_data[coordinate[1]].remove(coordinate[0])
            if not self.game_data[coordinate[1]]:
                del self.game_data[coordinate[1]]
        

    def find_all_adjacent(self):
        
        all_coordinates = set()
        adjacent_amount = {}
        
        for y in self.game_data:
            for x in self.game_data[y]:
                num_adjacent = 0
                
                for i in self.adjacent:
                    new_coordinate = (x + i[0], y + i[1])
                    if new_coordinate[1] in self.game_data and new_coordinate[0] in self.game_data[new_coordinate[1]]:
                        num_adjacent += 1
                    all_coordinates.add(new_coordinate)
                    
                adjacent_amount[(x, y)] = num_adjacent
                
        for coordinate in all_coordinates:
            if coordinate not in adjacent_amount:
                num_adjacent = 0
                
                for i in self.adjacent:
                    new_coordinate = (coordinate[0] + i[0], coordinate[1] + i[1])
                    if new_coordinate[1] in self.game_data and new_coordinate[0] in self.game_data[new_coordinate[1]]:
                        num_adjacent += 1
                        
                adjacent_amount[coordinate] = num_adjacent
                
        return adjacent_amount
    
    def step(self):
        
        self.generations += 1
        
        del self.store_data['lowest_x_val']
        adjacent_blocks = self.find_all_adjacent()
        
        for cell in adjacent_blocks:
            neighbours = adjacent_blocks[cell]
            alive = cell[1] in self.game_data and cell[0] in self.game_data[cell[1]]
            
            if not alive and neighbours == 3 or alive and 2 <= neighbours <= 3:
                self.add(cell)
            else:
                self.remove(cell)
    
    
    def display(self):
        for y in sorted(self.game_data.keys()):
            output = ''
            last_x = self.store_data['lowest_x_val']
            for x in sorted(list(self.game_data[y])):
                output += ' ' * max(0, (x - last_x)) + 'x'
                last_x = x + 1
            print output
