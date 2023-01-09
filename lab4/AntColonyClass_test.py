import unittest
import numpy as np
from AntColony import AntColony

class MyTestCase(unittest.TestCase):
    def setUp(self):
        distances = np.array([[np.inf, 2, 2, 5, 7],
                              [2, np.inf, 4, 8, 2],
                              [2, 4, np.inf, 1, 3],
                              [5, 8, 1, np.inf, 2],
                              [7, 2, 3, 2, np.inf]])
        self.ant_colony = AntColony(distances, 2, 2, 0.6, alpha=2, beta=4)

    def test_gen_path_distance(self):
        test_path = [(0, 1), (1, 4), (4, 3), (3, 2), (2, 0)]
        total_dist = self.ant_colony.gen_path_distance(test_path)
        self.assertEqual(total_dist, 9.0)
    def test_gen_path(self):
        path = self.ant_colony.gen_path(0)
        self.assertTrue(isinstance(path, list))
        self.assertTrue(isinstance(path[0], tuple))
    def test_run(self):
        all_time_shortest_path = self.ant_colony.run()
        self.assertTrue(isinstance(all_time_shortest_path[1], float))
        self.assertTrue(isinstance(all_time_shortest_path[0], list))
        self.assertTrue(isinstance(all_time_shortest_path[0][0], tuple))
