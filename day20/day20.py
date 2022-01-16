import os
import copy


class Field(object):
    def __init__(self):
        self.field = {}
        self.algo = []
        self.lit_pixels = 0
        self.default_pixel = 0
        self.min_row = self.min_col = float("inf")
        self.max_row = self.max_col = float("-inf")

    def add_row(self, row, row_idx):
        for col_idx, pixel in enumerate(row):
            self.set_pixel(row_idx, col_idx, 1 if pixel == "#" else 0)

    def set_algo(self, algo):
        for pixel in algo:
            self.algo.append(1 if pixel == "#" else 0)

    def set_pixel(self, row_idx, col_idx, value=None):
        self.max_row = max(self.max_row, row_idx)
        self.min_row = min(self.min_row, row_idx)
        self.max_col = max(self.max_col, col_idx)
        self.min_col = min(self.min_col, col_idx)

        if value is None:
            value = self.get_req_val(row_idx, col_idx)
        self.field[(row_idx, col_idx)] = value

        if value == 1:
            self.lit_pixels += 1

    def figure_out_default_pixel(self):
        self.default_pixel = self.get_req_val(self.min_col - 2, self.min_row - 2)

    def get_req_val(self, row_idx, col_idx):
        res = 0
        for i in range(row_idx - 1, row_idx + 2):
            for j in range(col_idx - 1, col_idx + 2):
                res = 2 * (res + self.field.get((i, j), self.default_pixel))
        return self.algo[res >> 1]

    def get_lit_pixels(self):
        return self.lit_pixels

    def clone(self):
        return copy.copy(self)


def process(total_iters, field):
    for _ in range(total_iters):

        new_field = Field()
        new_field.algo = field.algo
        new_field.default_pixel = field.default_pixel

        for row_idx in range(field.min_row - 1, field.max_row + 2):
            for col_idx in range(field.min_col - 1, field.max_col + 2):
                new_field.set_pixel(
                    row_idx, col_idx, field.get_req_val(row_idx, col_idx)
                )

        field = new_field.clone()
        field.figure_out_default_pixel()

    return field.get_lit_pixels()


def silver(field):
    return process(2, field)


def gold(field):
    return process(50, field)


def parse(lines):

    algorithm = []

    it = iter(lines)

    # parse algorithm
    for line in it:
        if line == "\n":
            break

        algorithm.append(line.strip())

    field = Field()
    field.set_algo("".join(algorithm))

    # parse initial image
    for row_idx, row in enumerate(it):
        field.add_row(row.strip(), row_idx)

    return field


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()
    field = parse(lines)

    return "DAY20", silver(field), gold(field)
