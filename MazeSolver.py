'''
Quick test so it currently only works with 2D mazes surrounded by bounding boxes,
later on I'll make it support any number of dimensions (easier), and different types of grids (harder).
'''

def edit_maze(maze, coordinate, value):
    maze[coordinate[1]] = maze[coordinate[1]][:coordinate[0]] + value + maze[coordinate[1]][coordinate[0] + 1:]

def solve_maze(start, end, maze, walkable=[' ']):
    maze_copy = [i for i in maze]
    paths = ((1, 0), (-1, 0), (0, 1), (0, -1))
    visited = []
    current_path = []
    current = start
    while True:
        #print 'Visiting ({}, {})'.format(current[0], current[1])
        edit_maze(maze_copy, current, '#')
        if current == end:
            print
            print 'Found exit:'
            current_path.append(current)
            edit_maze(maze_copy, start, 's')
            edit_maze(maze_copy, end, 'e')
            for i, coordinate in enumerate(current_path[1:-1]):
                next_coordinate = current_path[i + 2]
                if coordinate[1] < next_coordinate[1]:
                    edit_maze(maze_copy, coordinate, 'v')
                if coordinate[1] > next_coordinate[1]:
                    edit_maze(maze_copy, coordinate, '^')
                if coordinate[0] < next_coordinate[0]:
                    edit_maze(maze_copy, coordinate, '>')
                if coordinate[0] > next_coordinate[0]:
                    edit_maze(maze_copy, coordinate, '<')
            maze_copy = [line.replace('0', '-') for line in maze_copy]
            for line in maze_copy:
                print line
            return current_path
        
        #print visited
        visited.append(current)
        available_paths = []
        for i in paths:
            new_coordinate = (current[0] + i[0], current[1] + i[1])
            if new_coordinate in visited:
                continue
            cell = maze[new_coordinate[1]][new_coordinate[0]]
            if cell not in walkable:
                continue
            available_paths.append(new_coordinate)
        if available_paths:
            current_path.append(current)
            current = available_paths[0]
        else:
            current = current_path.pop()
            
            
maze = [
'00000000',
'0000  00',
'0  00 00',
'0 000  0',
'0     00',
'00 00000',
'00 00000',
'00000000'
]
start = (2, 6)
end = (2, 2)

print solve_maze(start, end, maze)
