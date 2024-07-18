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
import unittest
import pygame
from ddt import ddt, named_data
from main.GameofLife import World, DisplayWorld

@ddt
class TestGridMethods(unittest.TestCase):
    # set up 5x5 grid for test
    testworld = World(5,5)
    exp_grid = [['a','d','a','a','d'],['d','a','a','a','a'],
                ['a','a','d','a','a'],['a','d','d','a','d'],
                ['a','d','d','d','d']]

    # set up a 5x5 grid filled with test values
    def setUp(self):

        # set up 5x5 grid for test
        self.testworld.set_grid([['a','z','a','a','z'],['z','a','a','a','a'],
                    ['a','a','z','e','a'],['a','d','z','a','d'],
                    ['a','z','z','d','d']])

    # fill the 5x5 grid with dead cells as clean up
    def tearDown(self):
        self.testworld.set_grid([['d','d','d','d','d'],['d','d','d','d','d'],
                    ['d','d','d','d','d'],['d','d','d','d','d'],
                    ['d','d','d','d','d']])

    # test for neighbor_cell_counter method
    # list of data for the test.  Data list is in this format:
    # [name of the node using grid naming convention for the sides, x-coord of node,
    # y-coord of node, # of live neighbors around node]
    @named_data(['NW',0,0,3], ['N',2,0,5], ['NE',4,0,3],['int',2,2,6],
                ['W',0,2,4],['E',4,2,3],['SW',0,4,2],['S',2,4,3],
                ['SE',4,4,1])
    def test_neighbor_cell_counter(self, xpos, ypos, exp_value):
        self.assertEqual(self.testworld.neighbor_cell_counter(xpos,
                            ypos), exp_value)
       
    # test for get_cell method
    # list of data for the test.  Data list is in this format:
    # [cell type - alive, dead, etc, xpos of node, ypos of node,
    #  expected cell state - a, z, e, d]
    @named_data(['alive_cell',1,2,'a'],['zombie_cell',1,4,'z'],
                ['embryo_cell',3,2,'e'],['dead_cell',4,3,'d'],
                ['outside_NW_corner',-1,-1,'d'],['outside_SE_corner',
                5,5,'d'])
    def test_get_cell_state(self, xpos, ypos, exp_state):
        self.assertEqual(self.testworld.get_cell(xpos, ypos), exp_state)
    
    # test for set_cell method
    # list of data for the test.  Data list is in this format:
    # [type of transition, xpos of node, ypos of node, expected cell state]
    # e_to_a = embryo to alive 
    # a_to_z = alive to zombie
    # z_to_d = zombie to dead
    # d_to_e = dead to embryo
    @named_data(['e_to_a',3,2,'a'],['a_to_z',0,0,'z'],['z_to_d',2,4,'d'],
                ['d_to_e',4,3,'e'])
    def test_set_cell(self, xpos, ypos, exp_state):
        self.testworld.set_cell(xpos, ypos)
        self.assertEqual(self.testworld.get_cell(xpos, ypos), exp_state)
        
    # test for should_change method flags nodes that should change state
    # list of data for the test.  Data list is in this format:
    # [type of transition, xpos of node, ypos of node]
    # a_to_z = alive to zombie transition
    # d_to_z = dead to embryo transition
    @named_data(['a_to_z',1,1],['d_to_e',3,4])
    def test_should_change(self, xpos, ypos):
        self.assertTrue(self.testworld.should_change(xpos, ypos))
    
    # test 'a' cell can be left alone
    # should_change method should not flag nodes that 
    # aren't supposed to change state
    # list of data for the test.  Data list is in this format:
    # [type of transition, xpos of node, ypos of node]
    @named_data(['a',0,0],['d',4,3],['z',2,3],['e',3,2])
    def test_should_not_change(self, xpos, ypos):
        self.assertFalse(self.testworld.should_change(xpos, ypos))
        
    # test for is_zombie_or_embryo
    # method should flag z or e cells
    # list of data for the test.  Data list is in this format:
    # [type of cell, xpos of node, ypos of node]
    @named_data(['z',2,3],['e',3,2])
    def test_is_zombie_or_embryo(self, xpos, ypos):
        self.assertTrue(self.testworld.is_zombie_or_embryo(xpos, ypos))
        
    # test for is_zombie_or_embryo
    # method shouldn't flag a or d cells
    # list of data for the test.  Data list is in this format:
    # [type of cell, xpos of node, ypos of node]
    @named_data(['a',0,0],['d',4,3])
    def test_is_neither_zombie_or_embryo(self, xpos, ypos):
        self.assertFalse(self.testworld.is_zombie_or_embryo(xpos, ypos))
        
    # test to check clean up in second half step
    def test_clean_up_grid(self):
        self.testworld.clean_up_grid()
        self.assertListEqual(self.testworld.get_grid(),self.exp_grid)
        
class TestTransitionMethod(unittest.TestCase):
    # use 5x5 grid
    testworld = World(5,5)
    init_grid = [['d','a','d','d','a'],
            ['d','d','d','d','d'],['d','a','a','a','d'],
            ['d','d','a','d','d'],['a','d','d','d','a']]
    exp_grid_intermed = [['d','z','d','d','z'],
            ['d','e','d','e','d'],['d','a','a','a','d'],
            ['d','d','a','d','d'],['z','d','d','d','z']]

    def setUp(self):
        # set up 5x5 grid for test
        self.testworld.set_grid(self.init_grid)

    def tearDown(self):
        # fill the 5x5 grid with dead cells as clean up
        self.testworld.set_grid([['d','d','d','d','d'],
            ['d','d','d','d','d'],['d','d','d','d','d'],
            ['d','d','d','d','d'],['d','d','d','d','d']])
        

    # test for mark_for_transition method
    # test that nodes change to embryo or zombie cells in 1st half time step
    def test_mark_for_transition(self):
        self.testworld.mark_for_transition()
        self.assertListEqual(self.testworld.get_grid(),self.exp_grid_intermed)

class TestDisplayMethods(unittest.TestCase):
    
    init_grid = [['d','a','d','d','a'],
            ['d','d','d','d','d'],['d','a','a','a','d'],
            ['d','d','a','d','d'],['a','d','d','d','a']]
    exp_grid_final = [['d','d','d','d','d'],
            ['d','a','d','a','d'],['d','a','a','a','d'],
            ['d','d','a','d','d'],['d','d','d','d','d']]
    
    def setUp(self):
        # initialize world
        self.test_display_world = DisplayWorld(5, 5,'t', self.init_grid)
        
    def tearDown(self):
        #print(self.init_grid)
        pygame.quit()
        
    # test that the world is correct after 1 time step
    def test_world_after_one_time_step(self):
        self.test_display_world.world_loop()
        self.assertListEqual(self.test_display_world.game_world.get_grid(), 
                             self.exp_grid_final)
        
    # test that pygame is rendering the grid correctly
    def test_world_display_correctly(self):
        self.test_display_world.draw_world()
        self.assertListEqual(self.test_display_world.get_display_world(), 
                             self.init_grid)
        
    # test getter for window width
    def test_get_window_width(self):
        self.assertEqual(self.test_display_world.get_window_width(), 
                1250)
        
    # test getter for windows height
    def test_get_window_height(self):
        self.assertEqual(self.test_display_world.get_window_height(), 
                650)
        
    # test getter for container xpos in window coord
    # for xpos = 2
    def test_get_container_xpos(self):
        self.assertEqual(self.test_display_world.get_container_xpos(2), 
                         580)
        
    # test getter for container ypos in window coord
    # for ypos = 1
    def test_get_container_ypos(self):
        self.assertEqual(self.test_display_world.get_container_ypos(1), 
                         190)
        
    # test getter for container width
    def test_get_container_width(self):
        self.assertEqual(self.test_display_world.get_container_width(), 450)
        
    # test getter for container height
    def test_get_container_height(self):
        self.assertEqual(self.test_display_world.get_container_height(), 450)
        
    # test getter for cell size
    def test_get_cell_size(self):
        self.assertEqual(self.test_display_world.get_cell_size(), 90)

    # test getter for x coordinate of the container upper left corner
    def test_get_ulc_x(self):
        self.assertEqual(self.test_display_world.get_ulc_x(), 400)
        
    # test getter for y coordinate of the container upper left corner
    def test_get_ulc_y(self):
        self.assertEqual(self.test_display_world.get_ulc_y(), 100)
        
    # test getter for the container scale
    def test_get_scale(self):
        self.assertEqual(self.test_display_world.get_scale(), 90)
        
    # test getter for the margin
    def test_get_margin(self):
        self.assertEqual(self.test_display_world.get_margin(), 100)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()