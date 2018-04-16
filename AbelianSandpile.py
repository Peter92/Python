from __future__ import division
import numpy as np


class SandPile(object):
    
    ADJACENT = ((1, 0), (0, 1), (-1, 0), (0, -1))

    MAX_INT_LOW = 2**16 - 1
    
    MAX_INT_HIGH = 2**64 - 1
    
    def __init__(self, limit=None, height=4):
        """Create sand array and define an optional limit."""
        self.limit = limit
        self.size = 3
        self.height = height
        self._array = np.zeros((self.size, self.size), dtype=np.uint16)
        self._update_size(force_recalculate=True)

    def _update_size(self, size_increase=0, force_recalculate=False):
        """Increase the size of the grid if limits are not yet reached.
        Will return True/False depending if the size was changed.
        """
        #Handle limits
        if self.limit is not None:
            if self.limit == self.size:
                size_increase = 0
            else:
                size_increase = min(max(0, self.limit - self.size), size_increase)

        #Increase size
        if size_increase or force_recalculate:
            self._array = np.pad(self._array, size_increase, 'constant', constant_values=0)
            self.size = self._array.shape[0]
            self.midpoint = (self._array.shape[0]-1) // 2
            print 'Increased array size to {}'.format(self.size)
            return True
            
        return False

    def step(self):
        """Perform a single step of a collapse.
        Will return True until no extra steps are needed.
        """
        #Check if any points in sandpile are too high
        bool_match = self._array >= self.height
        if not np.any(bool_match):
            return False

        #Find where sandpile is too high
        matches = zip(*np.where(bool_match))
        
        offset = 0
        for y, x in matches:

            #Collapse the pile
            x += offset
            y += offset
            self._array[(x, y)] -= self.height
            
            for x_add, y_add in self.ADJACENT:
                new_x = x + x_add
                new_y = y + y_add

                #Coordinates too low
                if new_x < 0:
                    if self._update_size(-new_x):
                        offset -= new_x
                        self._array[(0, new_y-new_x)] += 1
                elif new_y < 0:
                    if self._update_size(-new_y):
                        offset -= new_y
                        self._array[(new_x-new_y, 0)] += 1
                        
                else:
                    #Coordinates in array
                    try:
                        self._array[(new_x, new_y)] += 1

                    #Coordinates too high
                    except IndexError:
                        max_difference = 1 + max(new_x, new_y) - self.size
                        if self._update_size(max_difference):
                            offset += max_difference
                            self._array[(new_x+max_difference, new_y+max_difference)] += 1
                
        return True

    def topple(self):
        """Collapse the sandpile until it comes to a rest."""
        count = 0
        while self.step():
            count += 1
        return self._array
                                
    def add(self, amount=1):
        """Drop any amount of sand in the middle of the pile.
        The toppling will be done
        """
        coordinate = (self.midpoint, self.midpoint)
        
        new_value = self._array[coordinate] + amount

        #Change datatype if resulting value is above the limit
        if new_value > self.MAX_INT_LOW:
            self._array = self._array.astype(np.uint64)

            #Split if integer is too large for numpy
            while new_value > self.MAX_INT_HIGH:
                self._array[coordinate] = self.MAX_INT_LOW
                new_value -= self.MAX_INT_LOW
                self.topple_pile()
                
            self._array[coordinate] += new_value
            self.topple()
            self._array = self._array.astype(np.uint16)

        else:
            self._array[coordinate] = new_value
            self.topple()

        return self._array

    def __str__(self):
        return str(self._array)

    def _display(self):
        """Very quick visual implementation."""
        import matplotlib.pyplot as plt
        plt.imshow(self._array.astype(np.float32), 'gray', None, 1, 'nearest')
        plt.show()


if __name__ == '__main__':
    sandpile = SandPile()
    sandpile.add(5000)
    sandpile._display()
