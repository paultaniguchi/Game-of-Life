'''
unit tests for GameofLife
Created on Apr 1, 2023
Grid sides naming convention

    N
  -----  
W |    | E
  -----
    S
@author: Paul
'''
import unittest
from GameofLife import World

class TestGridMethods(unittest.TestCase):
    # set up 5x5 grid for test
    testworld = World(5,5)

    # set up a 5x5 test grid filled with 1
    def setUp(self):
        # set up 5x5 grid for test
        self.testworld.set_grid([[1,1,1,1,1],[1,1,1,1,1],\
                                 [1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]])

    def tearDown(self):
        pass

    # counter for NW corner
    def test_neighbor_cell_counter_NW(self):
        self.assertEqual(self.testworld.neighbor_cell_counter(0,0),3)

    # counter for N edge
    def test_neighbor_cell_counter_N(self):
       self.assertEqual(self.testworld.neighbor_cell_counter(2,0),5)
        
    # counter for NE corner
    def test_neighbor_cell_counter_NE(self):
       self.assertEqual(self.testworld.neighbor_cell_counter(4,0),3)
       
    # counter for interior cell
    def test_neighbor_cell_counter_int(self):
       self.assertEqual(self.testworld.neighbor_cell_counter(2,2),8)       

    # counter for N edge
    def test_neighbor_cell_counter_W(self):
       self.assertEqual(self.testworld.neighbor_cell_counter(0,2),5)
       
    # counter for N edge
    def test_neighbor_cell_counter_E(self):
       self.assertEqual(self.testworld.neighbor_cell_counter(4,2),5)
       
    # counter for NW corner
    def test_neighbor_cell_counter_SW(self):
        self.assertEqual(self.testworld.neighbor_cell_counter(0,4),3)

    # counter for N edge
    def test_neighbor_cell_counter_S(self):
       self.assertEqual(self.testworld.neighbor_cell_counter(2,4),5)
        
    # counter for NE corner
    def test_neighbor_cell_counter_SE(self):
       self.assertEqual(self.testworld.neighbor_cell_counter(4,4),3)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()