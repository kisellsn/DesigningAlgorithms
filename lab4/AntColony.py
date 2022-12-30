import random as rp
import numpy as np
from numpy.random import choice as np_choice

class AntColony(object):

    def __init__(self, distances, n_ants, n_iterations, decay, alpha, beta):

        self._distances = distances
        self._pheromone = np.ones(self._distances.shape) / len(distances)
        self._all_inds = range(len(distances))
        self._n_ants = n_ants
        self._n_iterations = n_iterations
        self._decay = decay
        self._alpha = alpha
        self._beta = beta
        self._Lmin = self.gen_path_distance(self.gen_path(0,True)) #calc of the ideal solution price by a greedy algo

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self._n_iterations):
            print('\rCompleted: {}%'.format((i+1)*100/self._n_iterations), end='')
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths)
            shortest_path = min(all_paths, key=lambda x: x[1])

            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            self._pheromone = self._pheromone * self._decay

        return all_time_shortest_path

    def gen_all_paths(self):
        all_paths = []
        for i in range(self._n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_distance(path)))
        return all_paths

    def gen_path_distance(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self._distances[ele]
        return total_dist

    def gen_path(self, start,condition=False):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self._distances) - 1):
            if condition:
                move = self.pick_move_only_dist(self._pheromone[prev], self._distances[prev], visited)
            else:
                move = self.pick_move(self._pheromone[prev], self._distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # going back to home
        return path

    def spread_pheronome(self, all_paths):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths:
            for move in path:
                self._pheromone[move] += self._Lmin / self._distances[move]

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        row = pheromone ** self._alpha * (( 1.0 / dist) ** self._beta)
        norm_row = row / row.sum()
        move = np_choice(self._all_inds, 1, p=norm_row)[0]
        return move

    def pick_move_only_dist(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        for el in pheromone:
            el=1
        pheromone[list(visited)] = 0
        row = pheromone ** self._alpha * (( 1.0 / dist) ** self._beta)
        norm_row = row / row.sum()
        move = np.argmax(norm_row)
        return move
