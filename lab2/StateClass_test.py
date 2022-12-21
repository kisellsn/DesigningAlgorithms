from unittest import TestCase
from state import State

class TestState(TestCase):
  def setUp(self):
    self.stateTrue = State([2, 0, 3, 1])
    self.stateFalse = State([1, 2, 3, 1])

  def test_is_solution_True(self):
    self.assertTrue(self.stateTrue.is_solution())

  def test_is_solution_False(self):
    self.assertFalse(self.stateFalse.is_solution())

  def test_f1_heuristic(self):
    self.assertTrue(self.stateFalse > self.stateTrue)