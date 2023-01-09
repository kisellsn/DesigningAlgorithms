import math
import random
from scipy.spatial import distance


class BeeColony:
    def __init__(self, node_set):
        self.role = ''
        self.path = list(node_set) # зберігає всі вузли в кожній бджолі, рандомізує фуражирів
        self.distance = 0
        self.cycle = 0

def input_start_values():
    top_count = input('Enter the number of plots(min:10 max:500): ')
    while not top_count.isdigit() or (int(top_count) > 500 or int(top_count) < 10):
        top_count = input('Enter the number of plots(min:10 max:500): ')
    top_count = int(top_count)
    population = input('Enter the number of bees(min:10 max:1000): ')
    while not population.isdigit() or (int(population) > 1000 or int(population) < 10):
        population = input('Enter the number of bees(min:10 max:1000): ')
    population = int(population)

    cycle_limit = 100

    forager_percent = 0.5
    onlooker_percent = 0.5
    scout_percent = 0.2
    forager_limit = 1000
    role_percent = [onlooker_percent, forager_percent]
    scout_count = math.ceil(population * scout_percent)
    data = [[row, random.randint(5, 150), random.randint(5, 150)] for row in range(top_count)]#енерація відстаней(асиметрична мережа)

    return top_count,population,role_percent,scout_count,forager_limit,cycle_limit,data
def get_distance_between_nodes(n1, n2):
    """
    Обчислює евклідову відстань між двома вузлами.
    """
    return distance.euclidean(n1, n2)


def make_distance_table(data_list):
    """
    Створює таблицю, яка зберігає відстань між кожною парою вузлів.
    """
    length = len(data_list)
    table = [[get_distance_between_nodes(
        (data_list[i][1],data_list[i][2]), (data_list[j][1],data_list[j][2]))
        for i in range(0, length)] for j in range(0, length)]
    return table


def get_total_distance_of_path(path, table):
    """
    Обчислює загальну відстань шляху окремої бджоли.
    Завершується на початковому вузлі для завершення циклу.
    """
    new_path = list(path)
    new_path.insert(len(path), path[0])
    new_path = new_path[1:len(new_path)]

    coordinates = zip(path, new_path)
    distance = sum([table[i[0]][i[1]] for i in coordinates])
    return round(distance, 3)


def initialize_hive(population, data):
    """
    Ініціалізує вулик і заселяє його бджолами.
    Бджоли матимуть випадковий атрибут шляху.
    """
    path = [x[0] for x in data]
    hive = [BeeColony(path) for i in range (0, population)]
    return hive


def assign_roles(hive, role_percentiles, table):
    """
    Призначає початкові ролі на основі процентилів ролей
    кожній бджолі у вулику.
    Призначає рандомізований шлях бджолам-фуражирам.
    """
    population = len(hive)
    onlooker_count = math.floor(population * role_percentiles[0])
    forager_count = math.floor(population * role_percentiles[1])

    for i in range(0, onlooker_count):
        hive[i].role = 'O'

    for i in range(onlooker_count, (onlooker_count + forager_count)):
        hive[i].role = 'F'
        random.shuffle(hive[i].path)
        hive[i].distance = get_total_distance_of_path(hive[i].path, table)

    return hive

def mutate_path(path):
    """
    Отримує випадковий індекс від 0 до останнього елемента.
    Копіює шлях, міняє місцями два вузли, порівнює відстань.
    Повертає мутований шлях.
    """
    random_idx = random.randint(0, len(path) - 2)
    new_path = list(path)
    new_path[random_idx], new_path[random_idx + 1] = new_path[random_idx + 1], new_path[random_idx]
    return new_path

def forage(bee, table, limit):
    """
    Поведінка робочої бджоли, ітеративно уточнює потенційний найкоротший шлях
    шляхом заміни випадково вибраних сусідніх індексів.
    """
    new_path = mutate_path(bee.path)
    new_distance = get_total_distance_of_path(new_path, table)

    if new_distance < bee.distance:
        bee.path = new_path
        bee.distance = new_distance
        bee.cycle = 0 # скидаємо цикл, щоб бджола могла продовжувати прогресувати
    else:
        bee.cycle += 1
    if bee.cycle >= limit: # якщо бджола не прогресує
        bee.role = 'S'
    return bee.distance, list(bee.path)


def scout(bee, table):
    """
    Поведінка бджоли-розвідника, відмовляється від невдалого шляху на новий випадковий шлях.
    Скидає роль до фуражиру.
    """
    new_path = list(bee.path)
    random.shuffle(new_path)
    bee.path = new_path
    bee.distance = get_total_distance_of_path(new_path, table)
    bee.role = 'F'
    bee.cycle = 0


def waggle(hive, best_distance, table, forager_limit, scout_count):
    """
    Фіксує результати роботи бджіл-фуражирів,
    вибирає новий випадковий шлях для дослідження розвідників,
    повертає результати для оцінки сторонніми особами.
    """
    best_path = []
    results = []

    for i in range(0, len(hive)):
        if hive[i].role == 'F':
            distance, path = forage(hive[i], table, forager_limit)
            if distance < best_distance:
                best_distance = distance
                best_path = list(hive[i].path)
            results.append((i, distance))

        elif hive[i].role == 'S':
            scout(hive[i], table)

    # after processing all bees, set worst performers to scout
    results.sort(reverse = True, key=lambda tup: tup[1])
    scouts = [ tup[0] for tup in results[0:int(scout_count)] ]
    for new_scout in scouts:
        hive[new_scout].role = 'S'
    return best_distance, best_path


def recruit(hive, best_distance, best_path, table):
    """
    Набирає бджіл-спостерігачів, щоб знайти найкраще рішення.
    Повертає оновлені best_distance, best_path.
    """
    for i in range(0, len(hive)):
        if hive[i].role == 'O':
            new_path = mutate_path(best_path)
            new_distance = get_total_distance_of_path(new_path, table)
            if new_distance < best_distance:
                best_distance = new_distance
                best_path = new_path
    return best_distance, best_path


def print_details(cycle, path, distance, bee):
    print("Info about the shortest path: ")
    print("Cycle №: {}".format(cycle))
    print("Path: {}".format(path))
    print("Distance: {}".format(distance))
    print("Bee: {}".format(bee))
    print("\n")


