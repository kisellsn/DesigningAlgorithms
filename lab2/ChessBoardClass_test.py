from unittest import TestCase
from state import State
from ChessBoard import ChessBoard

class TestBoard(TestCase):
  def setUp(self):
    self.board = ChessBoard(4)

  def test_BFS_solution(self):
    state = State([1, 2, 3, 1])
    curr_state, iterations, total_states, states_in_mem, t = self.board.BFS_solution(state)
    self.assertEqual(curr_state.get_queens(), [2, 0, 3, 1])
    self.assertEqual(iterations,14)
    self.assertEqual(total_states, 53)
    self.assertEqual(states_in_mem, 39)

  def test_A_star_solution(self):
    state = State([2, 0, 2, 2])
    curr_state, iterations, total_states, states_in_mem, t = self.board.A_star_solution(state)
    self.assertEqual(curr_state.get_queens(), [1, 3, 0, 2])
    self.assertEqual(iterations,7)
    self.assertEqual(total_states, 25)
    self.assertEqual(states_in_mem, 18)

  def test_generate_queens(self):
    queens = self.board.generate_queens().get_queens()
    condition = True
    for num in queens:
      if int(num) >= self.board._n or int(num) < 0:
        condition = False
    self.assertTrue(condition)
    self.assertEqual(len(queens), self.board._n)

