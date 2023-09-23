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
from main.GameofLife import World

class TestTransitionMethod(unittest.TestCase):
    # use 5x5 grid
    testworld = World(5,5)
    exp_grid = [['d','z','d','d','z'],
            ['d','e','d','e','d'],['d','a','a','a','d'],
            ['d','d','a','d','d'],['z','d','d','d','z']]

    def setUp(self):
        # set up 5x5 grid for test
        self.testworld.set_grid([['d','a','d','d','a'],
            ['d','d','d','d','d'],['d','a','a','a','d'],
            ['d','d','a','d','d'],['a','d','d','d','a']])

    # fill the 5x5 grid with dead cells as clean up
    def tearDown(self):
        self.testworld.set_grid([['d','d','d','d','d'],
            ['d','d','d','d','d'],['d','d','d','d','d'],
            ['d','d','d','d','d'],['d','d','d','d','d']])

    # test for mark_for_transition method
    # test that nodes change to embryo or zombie cells in 1st half time step
    def test_mark_for_transition(self):
        self.testworld.mark_for_transition()
        self.assertListEqual(self.testworld.get_grid(),self.exp_grid)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()