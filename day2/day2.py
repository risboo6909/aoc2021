import os


def silver(lines):
    depth, position = 0, 0
    for line in lines:
        direction, magnitude = line.split()
        magnitude = int(magnitude)
        if direction == 'down':
            depth += magnitude
        elif direction == 'up':
            depth -= magnitude
        elif direction == 'forward':
            position += magnitude

    return depth * position


def gold(lines):
    depth, position, aim = 0, 0, 0
    for line in lines:
        direction, magnitude = line.split()
        magnitude = int(magnitude)
        if direction == 'down':
            aim += magnitude
        elif direction == 'up':
            aim -= magnitude
        elif direction == 'forward':
            position += magnitude
            depth += aim * magnitude

    return depth * position


def solve():
    lines = open(os.path.join(os.path.dirname(
        __file__), 'input'), 'rt').readlines()

    return "DAY 2", silver(lines), gold(lines)
