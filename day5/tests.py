import unittest
from day5.day5 import Line, Point, gen_points


class TestPointsGen(unittest.TestCase):
    def assert_points(self, res, exp):
        for i, point in enumerate(res):
            assert point == exp[i]

    def test_horiz(self):
        points = list(gen_points(Line(x1=0, y1=0, x2=2, y2=0)))
        self.assert_points(points, [Point(0, 0), Point(1, 0), Point(2, 0)])

        points = list(gen_points(Line(x1=1, y1=0, x2=-1, y2=0)))
        self.assert_points(points, [Point(1, 0), Point(0, 0), Point(-1, 0)])

    def test_vert(self):
        points = list(gen_points(Line(x1=0, y1=2, x2=0, y2=0)))
        self.assert_points(points, [Point(0, 2), Point(0, 1), Point(0, 0)])

        points = list(gen_points(Line(x1=3, y1=-1, x2=3, y2=-3)))
        self.assert_points(points, [Point(3, -1), Point(3, -2), Point(3, -3)])

    def test_diag(self):
        points = list(gen_points(Line(x1=-1, y1=-1, x2=1, y2=1)))
        self.assert_points(points, [Point(-1, -1), Point(0, 0), Point(1, 1)])

        points = list(gen_points(Line(x1=-1, y1=-1, x2=-3, y2=-3)))
        self.assert_points(points, [Point(-1, -1), Point(-2, -2), Point(-3, -3)])


if __name__ == "__main__":
    unittest.main()
