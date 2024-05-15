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
import pygame.freetype as freetype
from enum import Enum

#_black = (0,0,0)
#_white = (255,255,255)
#_beige = (245,245,220)
# _windows_width = 500
# _windows_height = 500
# _margin = 100
# delay between screen refresh
#_delay=1000

# where grid_type is
# t = Test Grid
# r = random grid
#_grid_type = 't'

def copy_nested_list(orig_list):
    '''
    copy nested list
    see https://www.iditect.com/programming/python-example/python-how-to-copy-a-nested-list.html
    Parameter
    orig_list = nested list
    '''
    return [lst.copy() for lst in orig_list]

class DisplayState(Enum):
    PAUSED = 0
    RUNNING = 1

# backend part that controls the critter growth
class World:
    
    grid = []
    
    # constructor - create the grid
    def __init__(self, ncol, nrow):
        self.numY = nrow
        self.numX = ncol
        self.grid = [ ['d' for _ in range(self.numX)] for _ in range(self.numY)]
    
    # seed grid with values from list
    def set_grid(self, in_list):
        if len(in_list) ==  self.numY and len(in_list[0]) == self.numX:
            # make a copy of in_list to avoid changing in_list
            # see https://www.iditect.com/programming/python-example/python-how-to-copy-a-nested-list.html
            self.grid = copy_nested_list(in_list)
        else:
            raise Exception("set_grid ERROR - incorrect list dimensions")
    
    # random pick which cells are alive / dead
    def set_random_grid(self):    
        for y in range(self.numY):
            for x in range(self.numX):
                self.set_random_cell(x, y)
   
    # getter for the grid
    def get_grid(self):
        return copy_nested_list(self.grid)
    
    # sum live & zombie neighboring cells that surround the target cell
    # for corner & edge nodes only sum neighbors that are 
    # within the grid
    def neighbor_cell_counter(self, xpos, ypos):
        cell_total = 0
        for y in range(-1,2):
            for x in range(-1,2):
                # skip over the target node
                if x==y and x == 0:
                    continue
                
                cell_state = self.get_cell(x+xpos,y+ypos)
                cell_total += (1 if (cell_state == 'a'
                        or cell_state == 'z') else 0)
                
                
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
            
    # set cell to a or d randomly
    def set_random_cell(self, x, y):
        self.grid[y][x] = 'a' if random.random() <= 0.5 else 'd'


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
    
    def __init__(self, nrow, ncol, init_cond_type, initial_grid=None):
        '''
        constructor - set up GUI window
             Parameters
             nrow 
             ncol
             grid : defaults to None so it can be optional
             init_cond_type
        '''
        
        # properties related to the GUI window
        self._container_width = 500
        self._container_height = 500
        self._margin = 100
        
        # colors
        self._black = (0,0,0)
        self._white = (255,255,255)
        self._beige = (245,245,220)  
        
        # delay between screen refresh
        self._delay=1000  
        
        # set state to RUNNING initially
        self.world_state = DisplayState.RUNNING 
        
        # initialize world
        self.game_world = World(nrow, ncol)
        
        self.cell_width = self._container_width // ncol
        self.cell_height = self._container_height // nrow
        pygame.init()
        self.scr = pygame.display.set_mode((self.get_window_width(), 
                        self.get_window_height()))
        self.scr.fill(self._beige)
        
        # background for time counter
        self.background = pygame.Surface(self.scr.get_size())
        self.background.fill(self._beige)
        
        # square at the center of the window
        pygame.draw.rect(self.scr, self._white,
            (self._margin, self._margin, self._container_width, self._container_height))
        
        # font for time counter
        self.font = freetype.Font(None)
        
        self.loop = True
        self.time_step = 0
        
        # put the initial population
        # test grid initial condition
        if initial_grid is None:
            display_world_grid = []
        else:
            display_world_grid = copy_nested_list(initial_grid)
            
        if init_cond_type == 't':
            # self.game_world = World(nrow, ncol)
            self.game_world.set_grid(display_world_grid)
        # random grid initial condition
        elif init_cond_type == 'r' or init_cond_type == 'u':
            # self.game_world = World(nrow, ncol)
            self.game_world.set_random_grid()
            
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
                    cell_color = self._black
                elif self.game_world.get_cell(x, y) == 'd':
                    cell_color = self._white
                else:
                    print("Invalid cell state")
                    exit()
                    
                pygame.draw.rect(self.scr, cell_color,
                        (self.get_container_xpos(x), self.get_container_ypos(y),
                         self.cell_width, self.cell_height))
    
    def get_display_world(self):            
        '''
        returns the node states based on the rendered grid
        '''
        displayed_grid = []
        
        for y in range(self.game_world.numY):
            temp_grid = []
            for x in range(self.game_world.numX):
                
                # get cell state based on the rendered node color
                if self.scr.get_at((self.get_container_xpos(x),
                    self.get_container_ypos(y))) == self._black:
                        temp_grid.append('a')
                else:
                    temp_grid.append('d')
                    
            displayed_grid.append(temp_grid)
        
        return displayed_grid
    
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
        
    def get_window_width(self):
        '''
        calculate overall width of GUI window
        '''
        return self._container_width+2*self._margin
    
    def get_window_height(self):
        '''
        calculate overall height of GUI window
        '''
        return self._container_height+2*self._margin
    
    def get_container_xpos(self, xpos):
        '''
        convert xpos from container coord sys to GUI window coord sys
        '''
        return xpos * self.cell_width+self._margin
    
    def get_container_ypos(self, ypos):
        '''
        convert xpos from container coord sys to GUI window coord sys
        '''
        return ypos * self.cell_height+self._margin
    
    def world_loop(self):
        '''
        for updating the world thru each time step
        '''       

        # event handling
        for event in pygame.event.get():
            # exit for the GUI window
            if event.type == pygame.QUIT:
                self.loop = False
            # temporarily use keyboard to pause / unpause world
            # press p to pause / press r to resume
            # TO DO - replace with button on GUI
            elif event.type == pygame.KEYDOWN:
                if ( event.key == pygame.K_p and 
                self.world_state == DisplayState.RUNNING ):
                    self.world_state = DisplayState.PAUSED
                elif ( event.key == pygame.K_r and 
                self.world_state == DisplayState.PAUSED ):
                    self.world_state = DisplayState.RUNNING
        
        if self.world_state == DisplayState.RUNNING:
            
            # draw world
            self.draw_world()
            pygame.time.delay(self._delay)
        
            # first half step
            self.game_world.mark_for_transition()
        
            # second half step
            self.game_world.clean_up_grid()
                
        # exit for the GUI window
        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        self.loop = False
        
        # self.clock.tick(60)
            # display current time step
            # move this outside if block for user-specified initial world?
            pygame.display.set_caption(f"Time = {self.get_time_step()}")
            # time counter in UI
            self.scr.blit(self.background,(self.get_window_width()/3,
                self.get_window_height()-self._margin/2))
            self.font.render_to(self.scr,
            (self.get_window_width()/3,self.get_window_height()-self._margin/2),
            f"Time = {self.get_time_step()}",self._black,size=20)
            pygame.display.flip()
        
            #update time
            self.update_time_step()

if __name__ == '__main__':
        
    # ask user for initial condition type
    init_type = input("Enter initial condition type (t/r): ")
    
    # for random grid - get grid dimensions first
    if init_type == 'r':
        nrow = int(input("Enter number of rows: "))
        ncol = int(input("Enter number of columns: "))
        my_world = DisplayWorld(nrow, ncol, init_type)
    # for test grid
    else:
        my_world = DisplayWorld(init_cond_type = init_type)
    
    my_world.main()