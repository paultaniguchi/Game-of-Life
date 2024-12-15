'''
unit tests for GameofLife
Created on Apr 1, 2023
Grid sides naming convention

    N
  -----  
W |    | E
  -----
    S
@author: Paul Taniguchi
'''
import pygame
from pytest import mark
from pytest import fixture
from main.GameofLife import World, DisplayWorld

class TestGridMethods():

    exp_grid = [['a','d','a','a','d'],['d','a','a','a','a'],
                ['a','a','d','a','a'],['a','d','d','a','d'],
                ['a','d','d','d','d']]
    
    @fixture
    def get_testworld(self):
        '''
        set up a 5x5 grid filled with test values        
        '''
        # set up 5x5 grid for test
        testworld = World(5,5)
        testworld.set_grid([['a','z','a','a','z'],['z','a','a','a','a'],
                    ['a','a','z','e','a'],['a','d','z','a','d'],
                    ['a','z','z','d','d']])
        yield testworld

        # fill the 5x5 grid with dead cells as clean up        
        testworld.set_grid([['d','d','d','d','d'],['d','d','d','d','d'],
                    ['d','d','d','d','d'],['d','d','d','d','d'],
                    ['d','d','d','d','d']])

    @mark.parametrize("xpos,ypos,exp_value",[(0,0,3),(2,0,5),(4,0,3),
            (2,2,6),(0,2,4),(4,2,3),(0,4,2),(2,4,3),(4,4,1)],
            ids=['NW','N','NE','int','W','E','SW','S','SE'])
    def test_neighbor_cell_counter(self, get_testworld, xpos, ypos, exp_value):
        '''
        test for neighbor_cell_counter method
        list of data for the test.  Data list is in this format:
        [name of the node using grid naming convention for the sides, x-coord of node,
        y-coord of node, # of live neighbors around node]
        '''
        assert get_testworld.neighbor_cell_counter(xpos,ypos) == exp_value

    @mark.parametrize("xpos, ypos, exp_state",[(1,2,'a'),(1,4,'z'),
            (3,2,'e'),(4,3,'d'),(-1,-1,'d'),(5,5,'d')],
            ids=['alive_cell','zombie_cell','embryo_cell','dead_cell',
                 'outside_NW_corner','outside_SE_corner'])
    def test_get_cell_state(self, get_testworld, xpos, ypos, exp_state):
        '''
        test for get_cell method
        list of data for the test.  Data list is in this format:
        [cell type - alive, dead, etc, xpos of node, ypos of node,
        expected cell state - a, z, e, d]
        '''
        assert get_testworld.get_cell(xpos, ypos) == exp_state
    
    @mark.parametrize("xpos, ypos, exp_state", [(3,2,'a'), (0,0,'z'),
                (2,4,'d'), (4,3,'e')], ids = ['e_to_a', 'a_to_z', 'z_to_d',
                'd_to_e'])
    def test_set_cell(self, get_testworld, xpos, ypos, exp_state):
        '''
        test for set_cell method
        list of data for the test.  Data list is in this format:
        [type of transition, xpos of node, ypos of node, expected cell state]
        e_to_a = embryo to alive 
        a_to_z = alive to zombie
        z_to_d = zombie to dead
        d_to_e = dead to embryo        
        '''
        get_testworld.set_cell(xpos, ypos)
        assert get_testworld.get_cell(xpos, ypos) == exp_state

    @mark.parametrize("xpos, ypos", [(1,1), (3,4)], ids = ['a_to_z', 'd_to_e'])
    def test_should_change(self, get_testworld, xpos, ypos):
        '''
        test for should_change method flags nodes that should change state
        list of data for the test.  Data list is in this format:
        [type of transition, xpos of node, ypos of node]
        a_to_z = alive to zombie transition
        d_to_z = dead to embryo transition
        '''
        assert get_testworld.should_change(xpos, ypos) is True
    
    @mark.parametrize("xpos, ypos", [(0,0), (4,3), (2,3), (3,2)],
            ids = ['a', 'd', 'z', 'e'])
    def test_should_not_change(self, get_testworld, xpos, ypos):
        '''
        test 'a' cell can be left alone
        should_change method should not flag nodes that 
        aren't supposed to change state
        list of data for the test.  Data list is in this format:
        [type of transition, xpos of node, ypos of node]        
        '''
        assert get_testworld.should_change(xpos, ypos) is False
        
    @mark.parametrize("xpos, ypos", [(2,3), (3,2)], ids = ['z', 'e'])
    def test_is_zombie_or_embryo(self, get_testworld, xpos, ypos):
        '''
        test for is_zombie_or_embryo
        method should flag z or e cells
        list of data for the test.  Data list is in this format:
        [type of cell, xpos of node, ypos of node]
        '''
        assert get_testworld.is_zombie_or_embryo(xpos, ypos) is True
       
    @mark.parametrize("xpos, ypos", [(0,0), (4,3)], ids = ['a', 'd'])
    def test_is_neither_zombie_or_embryo(self, get_testworld, xpos, ypos):
        '''
        test for is_zombie_or_embryo
        method shouldn't flag a or d cells
        list of data for the test.  Data list is in this format:
        [type of cell, xpos of node, ypos of node]        
        '''
        assert get_testworld.is_zombie_or_embryo(xpos, ypos) is False
        
    def test_clean_up_grid(self, get_testworld):
        '''
        test to check clean up in second half step        
        '''
        get_testworld.clean_up_grid()
        assert get_testworld.get_grid() == self.exp_grid

class TestTransitionMethod():
        
    @fixture
    def initialize_world(self, request):
        '''
        factory for setting up a test grid based on init_grid
        '''
        
        def _initialize_world(init_grid):   
            # set up grid based on init_grid dimensions
            testworld = World(len(init_grid[0]), len(init_grid))
        
            #initialize grid
            testworld.set_grid(init_grid)
            
            # use return instead of yield
            # yield doesn't return obj 
            return testworld
                        
        # teardown not necessary since testworld is local
        return _initialize_world        

    @mark.parametrize("init_grid,exp_grid_intermed", [(
            [['d','a','d','d','a'],['d','d','d','d','d'],
            ['d','a','a','a','d'],['d','d','a','d','d'],
            ['a','d','d','d','a']],
            [['d','z','d','d','z'],['d','e','d','e','d'],
            ['d','a','a','a','d'],['d','d','a','d','d'],
            ['z','d','d','d','z']]),
            ([['d','d','a'],['a','d','a'],['d','d','d'],
            ['d','a','a'],['a','a','a']],
            [['d','e','z'],['z','e','z'],['d','d','e'],
             ['e','z','a'],['a','z','a']])], 
             ids =['symmetric','asymmetric'])
    def test_mark_for_transition(self, initialize_world, init_grid, 
            exp_grid_intermed):
        '''
        test for mark_for_transition method
        test that nodes change to embryo or zombie cells in 1st half time step
        '''
        world = initialize_world(init_grid)
        world.mark_for_transition()
        assert world.get_grid() == exp_grid_intermed
        
class TestDisplayMethods():
    
    __init_symm_grid = [['d','a','d','d','a'],
            ['d','d','d','d','d'],['d','a','a','a','d'],
            ['d','d','a','d','d'],['a','d','d','d','a']]
    __init_asymm_grid = [['d','d','a'],['a','d','a'],['d','d','d'],
            ['d','a','a'],['a','a','a']]
    
    def get_display_world_grid(self, grid_type):
        '''
        return the symm or asymm grid depending on grid_type
        grid_type - 'symm' for the symmetric 5x5 world
                        'asymm' for the asymmetric 3x5 world
                        otherwise raise exception for wrong grid_type
        '''
        if grid_type == 'symm':
            return self.__init_symm_grid
        elif grid_type == 'asymm':
            return self.__init_asymm_grid
        else:
            raise ValueError("Incorrect grid type")
        
    @fixture
    def init_display_world(self, request):
        '''
        factory for initializing the display world
        '''
        
        def _init_display_world(grid_type):
            '''
            grid_type - 'symm' for the symmetric 5x5 world
                        'asymm' for the asymmetric 3x5 world
            '''

            grid = self.get_display_world_grid(grid_type)
            
            display_world = DisplayWorld(len(grid[0]), len(grid),'t', grid)
            return display_world
        
        yield _init_display_world
        
        pygame.quit()
    
    @mark.parametrize("grid_type,exp_grid_final",[('symm', 
            [['d','d','d','d','d'],['d','a','d','a','d'],
            ['d','a','a','a','d'],['d','d','a','d','d'],
            ['d','d','d','d','d']])])
    def test_world_after_one_time_step(self, init_display_world, grid_type, 
            exp_grid_final):
        '''
        test that the world is correct after 1 time step
        '''
        test_display_world = init_display_world(grid_type)
        test_display_world.world_loop()
        assert test_display_world.game_world.get_grid() == exp_grid_final
        
    @mark.parametrize("grid_type",[('symm'), ('asymm')])    
    def test_world_display_correctly(self, init_display_world, grid_type):
        '''
        test that pygame is rendering the grid correctly
        '''
        test_display_world = init_display_world(grid_type)
        test_display_world.draw_world()
        assert test_display_world.get_display_world() == \
                self.get_display_world_grid(grid_type)         

    def test_get_window_width(self, init_display_world):
        '''
        test getter for window width
        this doesn't need to be parametrized - window_width will be 
        the same for symm & asymm cases
        '''
        test_display_world = init_display_world('symm')
        assert test_display_world.get_window_width() == 1250
        
    def test_get_window_height(self, init_display_world):
        '''
        test getter for windows height
        this doesn't need to be parametrized - window_width will be 
        the same for symm & asymm cases        
        '''
        test_display_world = init_display_world('symm')
        assert test_display_world.get_window_height() == 650
    
        
    def test_get_container_xpos(self, init_display_world):
        '''
        test getter for container xpos in window coord
        for xpos = 2
        '''
        test_display_world = init_display_world('symm')
        assert test_display_world.get_container_xpos(2) == 580
        
    def test_get_container_ypos(self, init_display_world):
        '''
        test getter for container ypos in window coord
        for ypos = 1
        '''
        test_display_world = init_display_world('symm')
        assert test_display_world.get_container_ypos(1) == 190
        
    def test_get_container_width(self, init_display_world):
        '''
        test getter for container width
        '''
        test_display_world = init_display_world('symm')
        assert test_display_world.get_container_width() == 450
        
    def test_get_container_height(self, init_display_world):
        '''
        test getter for container height        
        '''
        test_display_world = init_display_world('symm')
        assert test_display_world.get_container_height() == 450      
    
    def test_get_cell_size(self, init_display_world):
        '''
        test getter for cell size        
        '''
        test_display_world = init_display_world('symm')
        assert test_display_world.get_cell_size() == 90  

    def test_get_ulc_x(self, init_display_world):
        '''
        test getter for x coordinate of the container upper left corner        
        '''
        test_display_world = init_display_world('symm')
        assert test_display_world.get_ulc_x() == 400

    def test_get_ulc_y(self, init_display_world):
        '''
        test getter for y coordinate of the container upper left corner        
        '''
        test_display_world = init_display_world('symm')
        assert test_display_world.get_ulc_y() == 100
    
    def test_get_scale(self, init_display_world):
        '''
        test getter for the container scale        
        '''
        test_display_world = init_display_world('symm')
        assert test_display_world.get_scale() == 90
    
    def test_get_margin(self, init_display_world):
        '''
        test getter for the margin        
        '''
        test_display_world = init_display_world('symm')
        assert test_display_world.get_margin() == 100
