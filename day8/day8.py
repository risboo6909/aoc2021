import os
from typing import List
from collections import namedtuple

Entry = namedtuple("Entry", "patterns, output")


def silver(parsed: List[Entry]):
    net = 0

    accept = [2, 3, 4, 7]

    for entry in parsed:
        for digit in entry.output:
            if len(digit) in accept:
                net += 1

    return net


def count_intersections(nums2segments, n, segments):
    return len(segments.intersection(nums2segments.get(n, set())))


def gold(parsed: List[Entry]):
    net = 0

    uniq_segments = {
        2: 1,
        3: 7,
        4: 4,
        7: 8,
    }

    for entry in parsed:

        nums2segments = {}

        # first scan for uniq segments
        for digit in entry.patterns + entry.output:
            l = len(digit)
            if l not in uniq_segments:
                continue

            number = uniq_segments[l]
            nums2segments[number] = set(digit)

        # scan for others
        for digit in entry.patterns + entry.output:

            l = len(digit)
            n = None

            segments = set(digit)

            if l == 5:
                if count_intersections(nums2segments, 1, segments) == 2:
                    n = 3
                elif count_intersections(nums2segments, 4, segments) == 3:
                    n = 5
                elif count_intersections(nums2segments, 8, segments) == 5:
                    n = 2

            elif l == 6 and count_intersections(nums2segments, 8, segments) == 6:
                if (
                    count_intersections(nums2segments, 4, segments) == 3
                    and count_intersections(nums2segments, 1, segments) == 1
                ):
                    n = 6
                elif count_intersections(nums2segments, 4, segments) == 4:
                    n = 9
                elif count_intersections(nums2segments, 1, segments) == 2:
                    n = 0

            if n is not None:
                nums2segments[n] = segments

        # build decimal number from digits online
        number = 0
        for digit in entry.output:
            for d, segments in nums2segments.items():
                if segments == set(digit):
                    number = number * 10 + d

        net += number

    return net


def parse(lines: List[str]) -> List[Entry]:
    res = []
    for line in lines:
        patterns, output = line.strip().split(" | ")
        res.append(Entry(patterns.split(), output.split()))

    return res


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    entries = parse(lines)

    return "DAY 8", silver(entries), gold(entries)
