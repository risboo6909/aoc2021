import os

from .helpers import (
    get_volume,
    find_intersection_volume,
    find_intersection_cuboid,
    Cuboid,
)

ON = "on"
OFF = "off"


class Board(object):
    def __init__(self):
        self.cuboids = []
        self.volume = None
        self.on_counter = 0

    def set_constraints(self, volume):
        self.volume = volume

    def modify_volume(self, new_cuboid):

        if self.volume and find_intersection_volume(
            new_cuboid, self.volume
        ) < get_volume(new_cuboid):
            return

        for cuboid in self.cuboids[:]:
            intersection_volume = find_intersection_volume(new_cuboid, cuboid)

            if intersection_volume > 0:
                if cuboid.state == ON:
                    self.cuboids.append(
                        find_intersection_cuboid(new_cuboid, cuboid, OFF)
                    )
                    self.on_counter -= intersection_volume
                else:
                    self.cuboids.append(
                        find_intersection_cuboid(new_cuboid, cuboid, ON)
                    )
                    self.on_counter += intersection_volume

        if new_cuboid.state == ON:
            self.cuboids.append(new_cuboid)
            self.on_counter += get_volume(new_cuboid)

    def active_cubes(self):
        return self.on_counter


def silver(cuboids):
    board = Board()

    volume = Cuboid("", x=(-50, 50), y=(-50, 50), z=(-50, 50))
    board.set_constraints(volume)

    for cuboid in cuboids:
        board.modify_volume(cuboid)

    return board.active_cubes()


def gold(cuboids):
    board = Board()

    for cuboid in cuboids:
        board.modify_volume(cuboid)

    return board.active_cubes()


def parse_length(length_str):
    range_str = length_str[2:]
    fromm, to = range_str.split("..")
    return int(fromm), int(to)


def parse(lines):
    cuboids = []

    for line in lines:
        state, lengths = line.strip().split()
        x_raw, y_raw, z_raw = lengths.split(",")
        cuboid = Cuboid(
            state=state,
            x=parse_length(x_raw),
            y=parse_length(y_raw),
            z=parse_length(z_raw),
        )
        cuboids.append(cuboid)

    return cuboids


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    cuboids = parse(lines)

    return "DAY22", silver(cuboids), gold(cuboids)
