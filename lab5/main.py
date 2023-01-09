import sys
from BeeColony import *

top_count,population,role_percent,scout_count,forager_limit,cycle_limit,data = input_start_values()

table = make_distance_table(data)
hive = initialize_hive(population, data)
assign_roles(hive, role_percent, table)

cycle = 1
best_distance = sys.maxsize
best_path = []
result = ()
while cycle < cycle_limit:
    print('\rCompleted: {}%'.format((cycle + 1) * 100 / cycle_limit), end='')
    waggle_distance, waggle_path = waggle(hive, best_distance, table, forager_limit, scout_count)
    if waggle_distance < best_distance:
        best_distance = waggle_distance
        best_path = list(waggle_path)
        #print_details(cycle, best_path, best_distance,'F')
        result = (cycle, best_path, best_distance,'F')

    recruit_distance, recruit_path = recruit(hive, best_distance, best_path, table)
    if recruit_distance < best_distance:
        best_distance = recruit_distance
        best_path = list(recruit_path)
        #print_details(cycle, best_path, best_distance,'R')
        result = (cycle, best_path, best_distance,'R')
    cycle += 1

print_details(result[0],result[1],result[2],result[3])

