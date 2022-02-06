from collections import namedtuple

Cuboid = namedtuple("Cuboid", "state x y z")


def axis_intersection(a_min, a_max, b_min, b_max):
    # we have to consider 4 cases
    if a_min >= b_min and b_max >= a_min and b_max <= a_max:
        # first case:
        #           a_min *----------* a_max
        #     b_min *---------* b_max
        return b_max - a_min + 1, a_min, b_max
    elif b_min >= a_min and b_min <= a_max and b_max >= a_max:
        # second case:
        #       a_min *----------* a_max
        #             b_min *--------* b_max
        return a_max - b_min + 1, b_min, a_max
    elif b_min >= a_min and b_max <= a_max:
        # third case:
        #   a_min *--------------------* a_max
        #         b_min *--------* b_max
        return b_max - b_min + 1, b_min, b_max
    elif a_min >= b_min and a_max <= b_max:
        # fourth case:
        #   b_min *--------------------* b_max
        #         a_min *--------* a_max
        return a_max - a_min + 1, a_min, a_max

    return 0, 0, 0


def find_intersection_volume(a, b):
    # finds volume of two cubes interesection
    side_x, _, _ = axis_intersection(a.x[0], a.x[1], b.x[0], b.x[1])
    side_y, _, _ = axis_intersection(a.y[0], a.y[1], b.y[0], b.y[1])
    side_z, _, _ = axis_intersection(a.z[0], a.z[1], b.z[0], b.z[1])
    return side_x * side_y * side_z


def find_intersection_cuboid(a, b, intersection_state):
    _, x_min, x_max = axis_intersection(a.x[0], a.x[1], b.x[0], b.x[1])
    _, y_min, y_max = axis_intersection(a.y[0], a.y[1], b.y[0], b.y[1])
    _, z_min, z_max = axis_intersection(a.z[0], a.z[1], b.z[0], b.z[1])
    return Cuboid(
        x=(x_min, x_max), y=(y_min, y_max), z=(z_min, z_max), state=intersection_state
    )


def get_volume(cuboid):
    size_x = cuboid.x[1] - cuboid.x[0] + 1
    size_y = cuboid.y[1] - cuboid.y[0] + 1
    size_z = cuboid.z[1] - cuboid.z[0] + 1
    return size_x * size_y * size_z
