from collections import Counter
from operator import itemgetter
import os


class Beacon(object):
    def __init__(self, x, y, z):
        self.coords = ((1, x), (2, y), (3, z))

    def __str__(self):
        return str(self.coords)

    def get_coords(self):
        return self.coords

    def apply_trns(self, coords, rotation):
        new_coords = [0, 0, 0]
        for i, axis_idx in enumerate(rotation):
            cur_axis, cur_pos = self.coords[abs(axis_idx) - 1]
            new_pos = -1 * cur_pos if axis_idx < 0 else cur_pos
            new_coords[i] = (
                cur_axis,
                new_pos + coords[i],
            )

        self.coords = tuple(new_coords)

    def gen_rotations(self):

        used = set()

        def rec():

            if len(used) == len(self.coords):
                return [()]

            all = []

            for i in range(len(self.coords)):

                if i in used:
                    continue

                used.add(i)
                for item in rec():
                    all.append((self.coords[i],) + item)
                    all.append(((-self.coords[i][0], -self.coords[i][1]),) + item)
                used.remove(i)

            return all

        return rec()


class Scanner(object):
    def __init__(self, label):
        self.label = label
        self.beacons = []
        self.translation_to = {}
        self.rotations = {}

    def add_beacon(self, x, y, z):
        self.beacons.append(Beacon(x, y, z))

    def apply_beacons_trns(self, coords, rot):
        for beacon in self.beacons:
            beacon.apply_trns(coords, rot)

    def set_translation_to(self, other, offset_x, offset_y, offset_z, rot_id):
        self.translation_to[other.label] = (
            (
                offset_x[0],
                offset_y[0],
                offset_z[0],
            ),
            rot_id,
        )

    def gen_rotations(self):
        all_rotations = [beacon.gen_rotations() for beacon in self.beacons]
        for i in range(len(all_rotations[0])):
            beacon_rotation = [rot[i] for rot in all_rotations]
            basis = tuple(all_rotations[0][i][j][0] for j in range(3))
            self.rotations[basis] = beacon_rotation


def find_offsets(first, second):

    for rot_id, rotation in second.rotations.items():
        delta_x = Counter()
        delta_y = Counter()
        delta_z = Counter()

        for beacon_first in first.beacons:
            for coords_other in rotation:
                coords_first = beacon_first.get_coords()
                delta_x[coords_first[0][1] - coords_other[0][1]] += 1
                delta_y[coords_first[1][1] - coords_other[1][1]] += 1
                delta_z[coords_first[2][1] - coords_other[2][1]] += 1

        offset_x = delta_x.most_common(1)[0]
        offset_y = delta_y.most_common(1)[0]
        offset_z = delta_z.most_common(1)[0]

        if offset_x[1] >= 12 and offset_y[1] >= 12 and offset_z[1] >= 12:
            second.set_translation_to(first, offset_x, offset_y, offset_z, rot_id)
            return


def traverse(origin, cur_beacon, beacon_map, visited):
    if cur_beacon == origin:
        return [[]]

    visited.add(cur_beacon.label)

    for label in cur_beacon.translation_to:

        if label in visited:
            continue

        res = traverse(origin, beacon_map[label], beacon_map, visited)
        if res:
            return [cur_beacon.translation_to[label]] + res

    return []


def origin_coords(trns_chains, scanner_map):
    coords_in_origin = {}

    for label, transforms in trns_chains.items():

        coords = [i for i in transforms[0][0]]
        coords_new = [0, 0, 0]

        scanner = scanner_map[label]

        # apply first transformation to beacons
        translate, rotate = transforms[0]
        scanner.apply_beacons_trns(translate, rotate)

        # apply rest transformations
        for translate, rotate in transforms[1:]:
            scanner.apply_beacons_trns(translate, rotate)
            for i, axis_idx in enumerate(rotate):
                coords_new[i] = coords[abs(axis_idx) - 1]
                if axis_idx < 0:
                    coords_new[i] *= -1
                coords_new[i] += translate[i]

            coords = coords_new[:]

        coords_in_origin[label] = coords

    return coords_in_origin


def silver(scanners):

    for scanner in scanners:
        scanner.gen_rotations()

    for first in scanners:
        for second in scanners:
            if first == second:
                continue
            find_offsets(first, second)

    origin = scanners[0]

    scanner_map = {}
    for scanner in scanners:
        scanner_map[scanner.label] = scanner

    translations = {}
    # compute path from each scanner to zero-scanner
    for scanner in scanners[1:]:
        trns_chain = traverse(origin, scanner, scanner_map, set())
        translations[scanner.label] = trns_chain[:-1]

    # apply transformation from each scanner to zero-scanner (origin)
    coords_in_origin = origin_coords(translations, scanner_map)

    # find uniq beacons
    uniq_beacons = set()
    for scanner in scanners:
        for beacon in scanner.beacons:
            uniq_beacons.add(tuple(map(itemgetter(1), beacon.get_coords())))

    return len(uniq_beacons), coords_in_origin


def manhattan(coords1, coords2):
    return (
        abs(coords1[0] - coords2[0])
        + abs(coords1[1] - coords2[1])
        + abs(coords1[2] - coords2[2])
    )


def gold(coords_in_origin):
    max_dist = 0

    for first in coords_in_origin.values():
        for second in coords_in_origin.values():
            tmp = manhattan(first, second)
            if tmp > max_dist:
                max_dist = tmp

    return max_dist


def parse(lines):

    scanners = []
    scanner = None
    idx = 0

    for line in lines:

        line = line.strip()

        if line == "":
            continue

        if line.startswith("---"):
            if scanner:
                scanners.append(scanner)

            scanner = Scanner(idx)
            idx += 1
        else:
            scanner.add_beacon(*list(map(int, line.split(","))))

    scanners.append(scanner)

    return scanners


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()
    parsed = parse(lines)
    silver_res, coords_in_origin = silver(parsed)
    return "DAY19", silver_res, gold(coords_in_origin)
