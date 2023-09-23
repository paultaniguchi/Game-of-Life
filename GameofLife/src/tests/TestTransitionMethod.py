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

class Test(unittest.TestCase):
    # set up 3x3 grid for test
    testworld = World(3,3)
    exp_grid = [['e','z','a'],['a','z','z'],\
                ['e','a','e']]

    def setUp(self):
        # set up 3x3 grid for test
        self.testworld.set_grid([['d','a','a'],['a','a','a'],\
                ['d','a','d']])


    def tearDown(self):
        pass


    def test_mark_for_transition(self):
        self.testworld.mark_for_transition()
        self.assertListEqual(self.testworld.grid,self.exp_grid)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()