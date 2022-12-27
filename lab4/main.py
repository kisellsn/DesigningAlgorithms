from AntColony import AntColony
import random
import numpy as np
from time import time

top_count = input('Enter the number of vertices(min:2 max:250): ')
while not top_count.isdigit() or (int(top_count) > 250 or int(top_count) < 2):
    top_count = input('Enter the number of vertices(min:2 max:250): ')

ant_count = input('Enter the number of ants(<number of vertices): ')
while not ant_count.isdigit() or (int(ant_count) > 250 or int(ant_count) < 1) or int(ant_count)>=int(top_count):
    ant_count = input('Enter the number of ants(<number of vertices): ')

distances = np.array([[np.inf if i == j else random.randint(1, 50) for j in range(int(top_count))] for i in range(int(top_count))])
for i in range(int(top_count)):
    for j in range(i, len(distances)):
        distances[j][i] = distances[i][j]

start_time = time()
ant_colony = AntColony(distances, int(ant_count), 100, 0.6, alpha=2, beta=4)
shortest_path = ant_colony.run()
print ("\n\nThe shortest way: {}".format(shortest_path[0]), "\nThe smallest distance: ",shortest_path[1])
print("Time: ",time()-start_time)