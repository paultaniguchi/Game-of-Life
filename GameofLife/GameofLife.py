'''
Created on Mar 30, 2023

cell values - 'd' : not alive
              'a' : alive
              'z' : zombie - marked for elimination in next time step
              'e' : embryo - alive in next time step

@author: Paul
'''

import random

class World():
    
    grid = []
    
    
    # constructor - create the grid
    def __init__(self, ncol, nrow):
        self.numY = nrow
        self.numX = ncol
        self.grid = [ ['d' for x in range(self.numX)] for y in range(self.numY)]
    
    # seed grid with values from list
    def set_grid(self, in_list):
        if len(in_list) ==  self.numY and len(in_list[0]) == self.numX:
            self.grid = in_list;
        else:
            print("ERROR - incorrect list dimensions")
    
    # update cells with new status at each time step
    
    # sum neighboring cells that surround the target cell
    # for corner & edge nodes only sum neighbors that are 
    # within the grid
    def neighbor_cell_counter(self, xpos, ypos):
        cell_total = 0
        # TO DO - skip over the target node
        # TO DO - handle zombie nodes
        for y in range(-1,2):
            for x in range(-1,2):
                # skip over the target node
                if x==y and x == 0:
                    continue
                
                cell_state = self.get_cell(x+xpos,y+ypos)
                cell_total += (1 if (cell_state == 'a'
                        or cell_state == 'z') else 0)
                
                #cell_total += (abs(self.grid[ypos+y][x+xpos]) if (\
                #(xpos+x) >= 0 and (xpos+x) < self.numX and \
                #(ypos+y) >= 0 and (ypos+y) < self.numY) else 0)
                
        return cell_total
    
    # return the state of the cell for pos x,y
    # if pos x,y is outside the grid, return dead
    def get_cell(self,x,y):
        
        if (x >= 0 and x < self.numX) and (y >= 0 and y < self.numY):
            return self.grid[y][x]
        else:
            return 'd'
    
    # 
        
    
    #display grid
    


if __name__ == '__main__':
    pass