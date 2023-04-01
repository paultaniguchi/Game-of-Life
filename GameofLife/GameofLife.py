'''
Created on Mar 30, 2023

cell values - 0 : not alive
              1 : alive
              -1 : zombie - marked for elimination

@author: Paul
'''

import random

class World():
    
    grid = []
    
    
    # constructor - create the grid
    def __init__(self, ncol, nrow):
        self.numY = nrow
        self.numX = ncol
        self.grid = [ [0 for x in range(self.numX)] for y in range(self.numY)]
    
    # seed grid
    
    
    # update cells with new status at each time step
    
    # sum neighboring cells that surround the target cell
    # for corner & edge nodes only sum neighbors that are 
    # within the grid
    def neighbor_cell_counter(self, xpos, ypos):
        cell_total = 0
        # TO DO - skip over the target node
        for x in range(-1,2):
            for y in range(-1,2):
                cell_total += (self.grid[xpos+x][y+ypos] if 
                (xpos+x) >= 0 and (xpos+x) < self.numX and 
                (ypos+y) >= 0 and (ypos+y) < self.numY and 
                (xpos == ypos ==0)
                else 0)
        return cell_total
        
    
    #display grid
    


if __name__ == '__main__':
    pass