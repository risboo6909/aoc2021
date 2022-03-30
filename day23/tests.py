import unittest
from day23.day23 import parse, Board

input = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""


class TestBoardMethods(unittest.TestCase):
    def setUp(self):
        self.board = parse(input.split(), 2)

    def test_pop_to_hall(self):
        assert self.board.pop_to_hall(7, 4) == 40

        assert self.board.hall[4] == "B"
        assert self.board.rooms[7][0] == "C"
        assert len(self.board.rooms[7]) == 1
