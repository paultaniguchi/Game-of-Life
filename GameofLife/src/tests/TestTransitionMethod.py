'''
unit tests for GameofLife
Created on Jun 3, 2023
Grid sides naming convention

    N
  -----  
W |    | E
  -----
    S

@author: Paul
'''
import unittest
import pygame
from main.GameofLife import World, DisplayWorld

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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()