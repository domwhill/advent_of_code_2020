"""Advent of code day 12


Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing.
"""
import re
import numpy as np
# star facing east


def get_manhatten_distance(position):
    return np.sum(np.abs(position))


def deg_to_radians(deg):
    return (deg / 360.0) * (2.0 * np.pi)


def radians_to_degree(rad):
    return (rad / (2.0 * np.pi)) * 360.0


def get_orientation_from_angle(deg):
    rad = deg_to_radians(deg)
    return np.array([np.cos(rad), np.sin(rad)])


def update_ship_orientation(ship_orientation, direction, step):
    position, angle = ship_orientation
    if direction in ("L", "R"):
        angle = update_angle(angle, direction, step)
    else:
        position = update_position(angle, direction, position, step)
    return (position, angle)


def update_ship_orientation_2(ship_position, waypoint_position, direction, step):

    if direction == "F":
        ship_position = update_ship_position(ship_position, waypoint_position, step)

    elif direction in ("L", "R"):
        waypoint_position = rotate_waypoint(direction, waypoint_position, step)

    else:
        waypoint_position = update_waypoint_position(direction, waypoint_position, step)
    return (ship_position, waypoint_position)


def update_position(angle, direction, position, step):
    direction_lookup = \
        {"N": np.array([0.0, 1.0]),
         "S": np.array([0.0, -1.0]),
         "E": np.array([1.0, 0.0]),
         "W": np.array([-1.0, 0.0]),
         "F": get_orientation_from_angle(angle)}
    position += direction_lookup[direction] * step
    return position


def update_waypoint_position(direction, position, step):
    direction_lookup = \
        {"N": np.array([0.0, 1.0]),
         "S": np.array([0.0, -1.0]),
         "E": np.array([1.0, 0.0]),
         "W": np.array([-1.0, 0.0])
         }
    position += direction_lookup[direction] * step
    return position


def rotate_waypoint(direction, position, step):
    angle_lookup = {"L": 1, "R": -1}
    step_rad = angle_lookup[direction] * deg_to_radians(step)

    R = np.array([[np.cos(step_rad), -np.sin(step_rad)], [np.sin(step_rad), np.cos(step_rad)]])

    new_waypoint = R.dot(position)
    return new_waypoint


def update_ship_position(ship_position, waypoint_position, step):
    ship_position += waypoint_position * step
    return ship_position


def update_angle(angle, direction, step):
    angle_lookup = {"L": 1, "R": -1}
    angle += angle_lookup[direction] * step
    return angle


def read_file(file_name):
    f = open(file_name, "r")
    data = f.readlines()
    f.close()
    return data


def main():
    file_name = "day12_test_input.txt"
    file_name = "day12_input.txt"

    data = read_file(file_name)
    position, angle = np.array([0.0, 0.0]), 0.0
    ship_orientation = (position, angle)
    for line in data:
        mline = re.search("^([A-Z])([0-9]+)", line)
        direction, step = mline.groups()[0], int(mline.groups()[1])
        ship_orientation = update_ship_orientation(ship_orientation, direction, step)

        print(f"ship_orientation = {ship_orientation} instruction = {direction}, {step}")

    print("final position = ", position, get_manhatten_distance(position))


def main2():
    file_name = "day12_test_input.txt"
    file_name = "day12_input.txt"

    data = read_file(file_name)
    ship_position = np.array([0.0, 0.0])
    waypoint_position = np.array([10.0, 1.0])

    for line in data:
        mline = re.search("^([A-Z])([0-9]+)", line)
        direction, step = mline.groups()[0], int(mline.groups()[1])
        ship_position, waypoint_position = update_ship_orientation_2(ship_position,
                                                                     waypoint_position, direction,
                                                                     step)
        print(f"ship_orientation = {ship_position}, waypoint_orientation = {waypoint_position}"
              f" instruction = {direction}, {step}")

    print("final position = ", ship_position, waypoint_position,
          get_manhatten_distance(ship_position))


if __name__ == "__main__":
    main2()
