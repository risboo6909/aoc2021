import os


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

    def __init__(self, hall, rooms, room_size):
        self.hall = hall
        self.rooms = rooms
        self.room_size = room_size

    def __str__(self):
        res = '#'*len(self.hall)+'\n'
        res += ''.join((s for s in self.hall))+'\n'

        res += ''.join((get(self.rooms[i], self.room_size-1)
                       if i in self.rooms else '#' for i in range(13)))+'\n'

        for k in range(self.room_size-2, -1, -1):
            res += '  #'+''.join((get(self.rooms[i], k)
                                  if i in self.rooms else '#' for i in range(3, 10))) + '#  \n'
        res += '  #########  '

        return res

    def __hash__(self):
        return hash((tuple(self.hall), tuple((k, tuple(v)) for k, v in self.rooms.items())))

    def __eq__(self, other):
        return self.hall == other.hall and self.rooms == other.rooms

    def clone(self):
        return Board(self.hall[:], {k: v[:] for k, v in self.rooms.items()}, self.room_size)

    def is_proper_room(self, req_room_idx, to_room_idx):
        if req_room_idx != to_room_idx:
            return False

        for amphipod in self.rooms[to_room_idx]:
            if Board.room_indices[amphipod] != to_room_idx:
                return False
        return True

    def has_obstacle(self, from_idx, to_idx):
        if to_idx >= from_idx:
            for i in range(from_idx+1, to_idx+1):
                if self.hall[i] != '.':
                    return True
        else:
            for i in range(to_idx, from_idx):
                if self.hall[i] != '.':
                    return True

        return False

    # pops item from room_idx and place it to dest_idx in the hall
    # return True if success and False otherwise
    def pop_to_hall(self, room_idx, to_idx):
        if self.hall[to_idx] != '.':
            return False

        if len(self.rooms[room_idx]) == 0:
            return False

        if to_idx in self.rooms:
            return False

        if self.has_obstacle(room_idx, to_idx):
            return False

        item = self.rooms[room_idx].pop()
        self.hall[to_idx] = item

        return energy[item] * (abs(room_idx - to_idx) + self.room_size-len(self.rooms[room_idx]))

    # get item from the hall and move it into the room
    def push_from_hall(self, from_idx, to_room_idx):
        if self.hall[from_idx] == '.':
            return False

        if len(self.rooms[to_room_idx]) == self.room_size:
            return False

        if Board.room_indices[self.hall[from_idx]] != to_room_idx:
            return False

        if not self.is_proper_room(Board.room_indices[self.hall[from_idx]], to_room_idx):
            return False

        if self.has_obstacle(from_idx, to_room_idx):
            return False

        item = self.hall[from_idx]
        self.rooms[to_room_idx].append(item)
        self.hall[from_idx] = '.'

        return energy[item] * (abs(from_idx - to_room_idx) + self.room_size-len(self.rooms[to_room_idx])+1)

    # get item from one room and put it into another room
    def room_to_room(self, from_room_idx, to_room_idx):
        if from_room_idx == to_room_idx:
            return False

        if len(self.rooms[from_room_idx]) == 0:
            return False

        if len(self.rooms[to_room_idx]) == self.room_size:
            return False

        if not self.is_proper_room(Board.room_indices[self.rooms[from_room_idx][-1]], to_room_idx):
            return False

        if self.has_obstacle(from_room_idx, to_room_idx):
            return False

        item = self.rooms[from_room_idx].pop()
        self.rooms[to_room_idx].append(item)

        return energy[item] * (abs(from_room_idx - to_room_idx) + self.room_size-len(self.rooms[from_room_idx]) + self.room_size-len(self.rooms[to_room_idx])+1)

    def is_done(self):
        for label, room_idx in Board.room_indices.items():
            if len(self.rooms[room_idx]) < self.room_size:
                return False
            for i in range(self.room_size):
                if self.rooms[room_idx][i] != label:
                    return False
        return True


def solver(board, max_depth):

    visited = {}

    min_so_far = [float('inf')]

    hall_range = [1, 2, 4, 6, 8, 10, 11]
    room_indices = Board.room_indices.values()

    def rec(cloned_board, total_energy, depth):

        if total_energy >= min_so_far[0]:
            return

        if total_energy >= visited.get(cloned_board, min_so_far[0]):
            return

        if depth > max_depth:
            return

        visited[cloned_board] = total_energy

        if cloned_board.is_done():
            min_so_far[0] = total_energy
            return

        # move from hall to room
        board = cloned_board.clone()
        for from_idx in hall_range:
            for room_idx in room_indices:
                energy_used = board.push_from_hall(from_idx, room_idx)
                if energy_used:
                    rec(board, total_energy + energy_used, depth+1)
                    board = cloned_board.clone()

        # pop from room to hall
        board = cloned_board.clone()
        for room_idx in room_indices:
            for to_idx in hall_range:
                energy_used = board.pop_to_hall(room_idx, to_idx)
                if energy_used:
                    rec(board, total_energy + energy_used, depth+1)
                    board = cloned_board.clone()

        # move from room to room
        board = cloned_board.clone()
        for from_room_idx in room_indices:
            for to_room_idx in room_indices:
                energy_used = board.room_to_room(from_room_idx, to_room_idx)
                if energy_used:
                    rec(board, total_energy + energy_used, depth+1)
                    board = cloned_board.clone()

    rec(board, 0, 0)

    return min_so_far[0]


def silver(board):
    return solver(board, 16)


def gold(board):
    return solver(board, 32)


def parse(lines, room_size):
    hall = list(lines[1].strip())

    room_indices = (i for i, s in enumerate(lines[2].strip()) if s != '#')

    rooms = [[s] if s != '.' else [] for s in lines[2].strip() if s != '#']
    for k in range(room_size-1):
        rooms = [[s] + rooms[i//2]
                 for i, s in enumerate(lines[3+k].strip()) if (i % 2) != 0]

    indices_2_rooms = {}
    for idx, room in zip(room_indices, rooms):
        indices_2_rooms[idx] = room

    board = Board(hall, indices_2_rooms, room_size)

    return board


def solve():
    lines_silver = open(os.path.join(os.path.dirname(
        __file__), "input_silver"), "rt").readlines()
    board_silver = parse(lines_silver, room_size=2)

    lines_gold = open(os.path.join(os.path.dirname(
        __file__), "input_gold"), "rt").readlines()
    board_gold = parse(lines_gold, room_size=4)

    result_silver = silver(board_silver)
    result_gold = gold(board_gold)

    return "DAY23", result_silver, result_gold
