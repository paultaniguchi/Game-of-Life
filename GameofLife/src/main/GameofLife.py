'''
Created on Mar 30, 2023

cell values - 'd' : not alive
              'a' : alive
              'z' : zombie - marked for elimination in next time step
              'e' : embryo - alive in next time step

@author: Paul
'''

import random
import pygame

_black = (0,0,0)
_white = (255,255,255)
_windows_width = 500
_windows_height = 500
# delay between screen refresh
_delay=5000
# corresponds to the 5 x 5 test grid
_test_nrow = 5
_test_ncol = 5
# where grid_type is
# t = Test Grid
# r = random grid
_grid_type = 't'

# backend part that controls the critter growth
class World:
    
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
            raise Exception("set_grid ERROR - incorrect list dimensions")
    
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
    
    # change the cell state
    # states can only change in this order
    #   e > a > z > d > e
    def set_cell(self,x,y):
        
        if self.get_cell(x, y) == 'e':
            self.grid[y][x] = 'a'
        elif self.get_cell(x, y) == 'a':
            self.grid[y][x] = 'z'
        elif self.get_cell(x, y) == 'z':
            self.grid[y][x] = 'd'
        else:
            self.grid[y][x] = 'e' 


    # determine if the cell state should be changed
    # based on current cell state & # of neighbors
    # return True if cell should change state
    # return False if cell should not change state
    def should_change(self, x, y):

        neighbor_count = self.neighbor_cell_counter(x, y)        
        # when cell is on
        if self.get_cell(x,y) == 'a':
            # change state when less than 2 neighbors or more than 3
            if neighbor_count < 2 or neighbor_count > 3:
                return True
            #otherwise leave alone
            else:
                return False
        # when cell is off
        elif self.get_cell(x, y) == 'd':
            # change state when there are 3 neighbors
            if neighbor_count == 3:
                return True
            else:
                return False
        # catch-all for other cell states - don't change cell state
        else:
            return False
        
    # identify zombie or embryo cells
    def is_zombie_or_embryo(self, x, y):
        cell_state = self.get_cell(x, y)
        if cell_state == 'z' or cell_state == 'e':
            return True
        else:
            return False
    
    # first half-step - mark cell for birth/death
    # change 'a' cell to 'z' if too crowded
    # change 'd' cell to 'e' if there are enough neighbors
    def mark_for_transition(self): 
        for y in range(self.numY):
            for x in range(self.numX):
                if self.should_change(x, y) == True:
                    self.set_cell(x, y)
        
    # send half-step kill off zombies & vivify embryo cells
    # change 'z' cells to 'd'
    # change 'e' cells to 'a'
    def clean_up_grid(self):
        for y in range(self.numY):
            for x in range(self.numX):
                if self.is_zombie_or_embryo(x, y) == True:
                    self.set_cell(x, y) 
    
# frontend part
"""
DisplayWorld defaults to _test_nrow x _test_ncol test grid
"""
class DisplayWorld:
    
    _test_grid = [['d','a','d','d','a'],
            ['d','d','d','d','d'],['d','a','a','a','d'],
            ['d','d','a','d','d'],['a','d','d','d','a']]
    
    def __init__(self, nrow=_test_nrow,ncol=_test_ncol,
                 init_cond_type=_grid_type):
        '''
        constructor - set up GUI window
        '''
        self.cell_width = _windows_width // ncol
        self.cell_height = _windows_height // nrow
        pygame.init()
        self.scr = pygame.display.set_mode((_windows_width, 
                        _windows_height))
        self.scr.fill(_white)
        #self.clock = pygame.time.Clock()
        self.loop = True
        self.time_step = 0
        
        # put the initial population
        # test grid initial condition
        if init_cond_type == 't':
            self.game_world = World(nrow, ncol)
            self.game_world.set_grid(self._test_grid)
        # random grid initial condition
        elif init_cond_type == 'r' or init_cond_type == 'u':
            self.game_world = World(nrow, ncol)
            
            # random grid initial condition
            # to do put in random grid
        # user selected initial condition
        else:
            raise Exception("incorrect initial condition type")
        
    def main(self):
        '''
        main loop for keeping the GUI window on screen
        '''
        while self.loop == True:
            self.world_loop()
        pygame.quit()
        
    def draw_world(self):
        '''
        draw white square if the cell is d
        draw black square if the cell is a
        '''
        for y in range(self.game_world.numY):
            for x in range(self.game_world.numX):
                
                # get cell state to determine cell color
                if self.game_world.get_cell(x, y) == 'a':
                    cell_color = _black
                elif self.game_world.get_cell(x, y) == 'd':
                    cell_color = _white
                else:
                    print("Invalid cell state")
                    exit()
                    
                pygame.draw.rect(self.scr, cell_color,
                        (x * self.cell_width, y * self.cell_height,
                         self.cell_width, self.cell_height))
                
    def get_time_step(self):
        '''
        return current time step
        '''
        return self.time_step    
    
    def update_time_step(self):
        '''
        increment time step
        '''
        self.time_step+=1
    
    def world_loop(self):
        '''
        for updating the world thru each time step
        '''       
        
        # draw world
        self.draw_world()
        pygame.time.delay(_delay)
        
        # first half step
        self.game_world.mark_for_transition()
        
        # second half step
        self.game_world.clean_up_grid()
                
        # exit for the GUI window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.loop = False
        
        # self.clock.tick(60)
        # display current time step
        pygame.display.set_caption(f"Time = {self.get_time_step()}")
        pygame.display.flip()
        
        #update time
        self.update_time_step()


if __name__ == '__main__':
        
    # ask user for initial condition type
    init_type = input("Enter initial condition type (t/r): ")
    
    # for random grid - get grid dimensions first
    if init_type == 'r':
        nrow = input("Enter number of rows: ")
        ncol = input("Enter number of columns: ")
        my_world = DisplayWorld(nrow, ncol, init_type)
    # for test grid
    else:
        my_world = DisplayWorld(init_cond_type = init_type)
    
    my_world.main()