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
        self.testworld.set_grid([['a','z','a','a','z'],['z','a','a','a','a'],\
                    ['a','a','z','e','a'],['a','d','z','a','d'],\
                    ['a','z','z','d','d']])

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
       self.assertEqual(self.testworld.neighbor_cell_counter(2,2),6)       

    # counter for W edge
    def test_neighbor_cell_counter_W(self):
       self.assertEqual(self.testworld.neighbor_cell_counter(0,2),4)
       
    # counter for E edge
    def test_neighbor_cell_counter_E(self):
       self.assertEqual(self.testworld.neighbor_cell_counter(4,2),3)
       
    # counter for SW corner
    def test_neighbor_cell_counter_SW(self):
        self.assertEqual(self.testworld.neighbor_cell_counter(0,4),2)

    # counter for S edge
    def test_neighbor_cell_counter_S(self):
       self.assertEqual(self.testworld.neighbor_cell_counter(2,4),3)
        
    # counter for SE corner
    def test_neighbor_cell_counter_SE(self):
       self.assertEqual(self.testworld.neighbor_cell_counter(4,4),1)
       
    # test for an alive cell
    def test_get_cell_alive(self):
        self.assertEqual(self.testworld.get_cell(1,2), 'a')
        
    # test for a zombie cell
    def test_get_cell_zombie(self):
        self.assertEqual(self.testworld.get_cell(1,4), 'z')
        
    # test for an embryo cell
    def test_get_cell_embryo(self):
        self.assertEqual(self.testworld.get_cell(3,2), 'e')
 
    # test for a dead cell
    def test_get_cell_dead(self):
        self.assertEqual(self.testworld.get_cell(4,3), 'd')
        
    # tests for a cell outside the grid
    def test_get_cell_outside_NW(self):
        self.assertEqual(self.testworld.get_cell(-1,-1), 'd')
        
    def test_get_cell_outside_SE(self):
        self.assertEqual(self.testworld.get_cell(self.testworld.numX,\
                self.testworld.numY), 'd')
    
    # test cell can go from e to a state:
    def test_set_cell_e_to_a(self):
        self.testworld.set_cell(3, 2)
        self.assertEqual(self.testworld.get_cell(3, 2), 'a')
        
    # test cell can go from a to z state:
    def test_set_cell_a_to_z(self):
        self.testworld.set_cell(0, 0)
        self.assertEqual(self.testworld.get_cell(0, 0), 'z')
        
    # test cell can go from z to d state:
    def test_set_cell_z_to_d(self):
        self.testworld.set_cell(2, 4)
        self.assertEqual(self.testworld.get_cell(2, 4), 'd')
        
    # test cell can go from d to e state:
    def test_set_cell_d_to_e(self):
        self.testworld.set_cell(4, 3)
        self.assertEqual(self.testworld.get_cell(4, 3), 'e')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()