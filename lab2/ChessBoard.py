import random
from queue import Queue, PriorityQueue
from time import time
from state import State


class ChessBoard:
    def __init__(self, n):
        self._n = n

    def input_queens(self):
        while True:
            s = input(f"Enter {self._n} queens in format '1 1 1 1 1 1'(from 0 to {self._n-1}): ")
            condition = True
            queens = s.split()
            for num in queens:
                if not num.isdigit():
                    condition = False
                elif int(num) >= self._n:
                    condition = False

            if len(s.replace(' ', '')) == self._n and condition:
                break
        queens = list(map(int, s.split()))
        state = State(queens)
        return state


    def generate_queens(self):
        queens = [random.randint(0, self._n - 1) for x in range(self._n)]
        state = State(queens, 0)
        return state

    def print_state(self, state: State):
        nums = ''.join(str(x) + ' ' * 5 if x < 9 else str(x) + ' ' * 4 for x in range(self._n))
        print('\n       ' + nums, end='')
        print('\n    -' + '------' * self._n)
        queens = state.get_queens()
        for i in range(self._n):
            text = f'{i}   ' if i < 10 else f'{i}  '
            print(text, end='')
            print('|  ', end='')
            for j in range(self._n):
                if queens[j] == i:
                    print('Q', end='')
                    print('  |  ', end='')
                else:
                    print('   |  ', end='')
            print('\n    -' + '------' * self._n)

        print(f"Queens: {queens}")

    def BFS_solution(self, initial_state):
        start_time = time()
        q = Queue()
        q.put(initial_state)

        iterations = 0
        total_states = 1
        states_in_mem = 1

        while not q.empty():

            if time() - start_time >= 1800:
                print('Time limit!')
                return False

            iterations += 1
            curr_state = q.get()
            states_in_mem -= 1

            if curr_state.is_solution():
                return curr_state, iterations, total_states, states_in_mem, time() - start_time

            curr_depth = curr_state.get_depth()
            if curr_depth != self._n:
                for i in range(self._n):
                    new_state = State(curr_state.get_queens(), curr_depth + 1)
                    new_state.move(curr_depth, i)  # queens[row] = col
                    q.put(new_state)
                    total_states += 1
                    states_in_mem += 1

    def A_star_solution(self, initial_state):
        start_time = time()
        q = PriorityQueue()
        q.put(initial_state)

        iterations = 0
        total_states = 1
        states_in_mem = 1

        while not q.empty():

            if time() - start_time >= 1800:
                return False

            iterations += 1
            curr_state = q.get()
            states_in_mem -= 1

            if curr_state.is_solution():
                return curr_state, iterations, total_states, states_in_mem, time() - start_time

            curr_depth = curr_state.get_depth()
            if curr_depth != self._n:
                for i in range(self._n):
                    new_state = State(curr_state.get_queens(), curr_depth + 1)
                    new_state.move(curr_depth, i)  # queens[row] = col
                    q.put(new_state)
                    total_states += 1
                    states_in_mem += 1
