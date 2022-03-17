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
        self.board = parse(input.split())

    def test_pop_to_hall(self):
        assert self.board.pop_to_hall(7, 4) == True

        assert self.board.hall[4] == 'B'
        assert self.board.rooms[7][0] == 'C'
        assert len(self.board.rooms[7]) == 1

    def room_to_room(self):
        assert self.board.room_to_room(5, 7) == True

        assert self.board.rooms[5][0] == 'D'
        assert len(self.board.rooms[5]) == 1
        assert self.board.rooms[7][1] == 'C'
        assert self.board.rooms[7][0] == 'C'
        assert len(self.boards.rooms) == 2

    def test_wrong_room(self):
        # TODO
        pass

    def test_many_steps(self):
        assert self.board.pop_to_hall(7, 4) == True
        assert self.board.room_to_room(5, 7) == True
        assert self.board.pop_to_hall(5, 6) == True
        assert self.board.push_from_hall(4, 5) == True
        assert self.board.room_to_room(3, 5) == True
        assert self.board.pop_to_hall(9, 8) == True
        assert self.board.pop_to_hall(9, 10) == True

        # check intersection here
        assert self.board.push_from_hall(6, 9) == False

        assert self.board.push_from_hall(8, 9) == True
        assert self.board.push_from_hall(6, 9) == True

        # room is full (error)
        assert self.board.push_from_hall(10, 5) == False

        assert self.board.push_from_hall(10, 3) == True
