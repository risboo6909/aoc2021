import os
import copy
#import sys

#sys.setrecursionlimit(1000)


energy = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

def get(xs, i):
    if len(xs) > i:
        return xs[i]
    return '.'


class Board(object):

    room_indices = {
        'A': 3,
        'B': 5,
        'C': 7,
        'D': 9,
    }

    def __init__(self, hall, rooms):
        self.hall = hall
        self.rooms = rooms

    def __str__(self):
        res = '#'*len(self.hall)+'\n'
        res += ''.join((s for s in self.hall))+'\n'
        res += ''.join((get(self.rooms[i], 1)
                       if i in self.rooms else '#' for i in range(13)))+'\n'
        res += '  #'+''.join((get(self.rooms[i], 0)
                              if i in self.rooms else '#' for i in range(3, 10))) + '#  \n'
        res += '  #########  '

        return res

    def __hash__(self):
        return hash(tuple(self.hall) + tuple((k, tuple(v)) for k, v in self.rooms.items()))

    def __eq__(self, other):
        return self.hall == other.hall and self.rooms == other.rooms 

    def clone(self):
        return Board(self.hall[:], copy.deepcopy(self.rooms))

    def has_obstacle(self, from_idx, to_idx):
        if to_idx >= from_idx:
            return any(self.hall[i] != '.' for i in range(from_idx+1, to_idx+1))

        return any(self.hall[i] != '.' for i in range(to_idx, from_idx))

    # pops item from room_idx and place it to dest_idx in the hall
    # return True if success and False otherwise
    def pop_to_hall(self, room_idx, to_idx):
        assert room_idx in self.rooms
        assert to_idx > 0 and to_idx < 13

        if self.hall[to_idx] != '.':
            return False

        if len(self.rooms[room_idx]) == 0:
            return False

        if to_idx in self.rooms.keys():
            return False

        if self.has_obstacle(room_idx, to_idx):
            return False

        item = self.rooms[room_idx].pop()
        self.hall[to_idx] = item

        return energy[item] * (abs(room_idx - to_idx) + 2-len(self.rooms[room_idx]))

    # get item from the hall and move it into the room
    def push_from_hall(self, from_idx, room_idx):
        assert room_idx in self.rooms
        assert from_idx > 0 and from_idx < 13
        # assert Board.home_indices[self.hall[from_idx]] == room_idx

        if self.hall[from_idx] == '.':
            return False

        if len(self.rooms[room_idx]) == 2:
            return False

        if Board.room_indices[self.hall[from_idx]] != room_idx:
            return False

        if len(self.rooms[room_idx]) == 1 and self.room_indices[self.rooms[room_idx][-1]] != room_idx:
            return False

        if self.has_obstacle(from_idx, room_idx):
            return False

        item = self.hall[from_idx]
        self.rooms[room_idx].append(item)
        self.hall[from_idx] = '.'

        return energy[item] * (abs(from_idx - room_idx) + 3-len(self.rooms[room_idx]))

    # get item from one room and put it into another room
    def room_to_room(self, from_idx, to_idx):
        assert from_idx in self.rooms
        assert to_idx in self.rooms

        if len(self.rooms[from_idx]) == 0:
            return False
            
        if len(self.rooms[to_idx]) == 2:
            return False
        # assert self.home_indices[self.rooms[from_idx][-1]] == to_idx

        if len(self.rooms[to_idx]) == 1 and self.room_indices[self.rooms[to_idx][-1]] != to_idx:
            return False

        if self.has_obstacle(from_idx, to_idx):
            return False

        item = self.rooms[from_idx].pop()
        self.rooms[to_idx].append(item)

        return energy[item] * (abs(from_idx - to_idx) + 2-len(self.rooms[from_idx]) + 3-len(self.rooms[to_idx]))


    def is_done(self):
        for label, room_idx in Board.room_indices.items():
            if len(self.rooms[room_idx]) < 2 or self.rooms[room_idx][0] != label or self.rooms[room_idx][1] != label:
                return False

        return True


def silver(board):
    visited = {}

    inf = float('inf')
    min_so_far = [inf]

    def rec(cloned_board, total_energy):

        if total_energy > 13000:
            return

        if total_energy >= min_so_far[0]:
            return

        if total_energy >= visited.get(cloned_board, inf):
            return

        #print(cloned_board, total_energy, end='\n\n')

        visited[cloned_board] = total_energy

        if cloned_board.is_done():
            min_so_far[0] = total_energy
            print(total_energy)
            print(cloned_board, end='\n')
            return

        # pop from room to hall
        board = cloned_board.clone()
        for room_idx in Board.room_indices.values(): 
            for to_idx in range(1, 12):
                energy_used = board.pop_to_hall(room_idx, to_idx)
                if energy_used:
                    rec(board, total_energy + energy_used)
                    board = cloned_board.clone()

        # move from hall to room
        board = cloned_board.clone()
        for from_idx in range(1, 12):
            # if board.hall[from_idx] == '.':
            #     continue
            for room_idx in Board.room_indices.values():
                energy_used = board.push_from_hall(from_idx, room_idx)
                if energy_used:
                    rec(board, total_energy + energy_used)
                    board = cloned_board.clone()

        # move from room to room
        board = cloned_board.clone()
        for from_room_idx in Board.room_indices.values():
            for to_room_idx in Board.room_indices.values():
                energy_used = board.room_to_room(from_room_idx, to_room_idx)
                if energy_used:
                    rec(board, total_energy + energy_used)
                    board = cloned_board.clone()

    rec(board, 0)
    
    print(min_so_far)

def gold(parsed):
    pass


def parse(lines):
    hall = list(lines[1].strip())

    room_indices = (i for i, s in enumerate(lines[2].strip()) if s != '#')
    rooms = [[s] if s != '.' else [] for s in lines[2].strip() if s != '#']
    rooms = [[s] + rooms[i//2]
             for i, s in enumerate(lines[3].strip()) if (i % 2) != 0]

    indices_2_rooms = {}
    for idx, room in zip(room_indices, rooms):
        indices_2_rooms[idx] = room

    board = Board(hall, indices_2_rooms)

    return board


def solve():
    lines = open(os.path.join(os.path.dirname(
        __file__), "input"), "rt").readlines()

    board = parse(lines)
    return "DAY23", silver(board), gold(board)
