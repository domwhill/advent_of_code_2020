"""
floor .
empty seat L
occupied seat #


Seat is empty and there are NO occupied seats adjacent to it it becomes occupied

seat is occupied and there are 4 or more seats adjacent to
 it that are also occupied it becomes empty
"""
import numpy as np


def load_data(fname):
    """Load in the test data from file."""
    f = open(fname, "r")
    data = f.readlines()
    f.close()

    line_length = find_line_length(data[0])
    array_data = []
    print("id = ", line_length)
    for il, line in enumerate(data):
        array_data.append(list(data[il])[:line_length])
    return np.array(array_data)


def find_line_length(line):
    """Find length of test data line.    """
    if " " not in list(line):
        # minus 1 here to remove newline characters
        id = len(line) - 1
    else:
        id = np.where(np.array(list(line)) == " ")[0][0]
    return id


def get_directions():
    window = [[iy, ix] for iy in range(-1, 2) for ix in range(-1, 2)]
    window.remove([0, 0])
    return np.array(window)


def construct_window_part2():
    window = [[iy, ix] for iy in range(-1, 2) for ix in range(-1, 2)]
    window.remove([0, 0])
    return np.array(window)


def pad_data(data):
    rows, cols = (data.shape[0] + 2, data.shape[1] + 2)
    pad_array = np.array([["."] * cols] * rows)
    pad_array[1:-1, 1:-1] = data
    return pad_array


def count_type(arr, value):
    if isinstance(arr, np.ndarray):
        count = np.sum(arr == value)
    elif isinstance(arr, list):
        count = arr.count(value)
    else:
        raise TypeError("value not recognised")
    return count


def swap_seats(padded_array, directions, question_part):
    swap_l = []
    swap_h = []
    ny, nx = padded_array.shape
    if question_part == 2:
        min_allowed_full_seats = 5
    else:
        min_allowed_full_seats = 4

    for ix in range(1, nx - 1):
        for iy in range(1, ny - 1):
            val = padded_array[iy, ix]
            if val == ".":
                continue

            _subset = get_subset(padded_array, directions, iy, ix, question_part)

            num_empty = count_type(_subset, "L")
            num_full = count_type(_subset, "#")
            if val == "L" and num_full == 0:
                swap_l.append((iy, ix))
            elif val == "#" and num_full >= min_allowed_full_seats:
                swap_h.append((iy, ix))

    padded_array = swap_full_and_empty(padded_array, swap_h, swap_l)

    return padded_array, swap_l, swap_h


def get_subset(array, directions, iy, ix, question_part):
    if question_part == 1:
        _subset = get_subset_part1(array, directions, iy, ix)
    elif question_part == 2:
        _subset = get_subset_part2(array, directions, iy, ix)
    else:
        raise ValueError(f"Question part {question_part} not recognised")
    return _subset


def get_subset_part1(array, directions, iy, ix):
    """Search all 8 directions to return the valid adjacent seats."""
    indx = directions + np.array([iy, ix])
    _subset = [array[i1, i2] for (i1, i2) in indx]
    return _subset


def in_bounds(idx, limit):
    """Returns false if index is not in the central domain"""
    return (idx > 0) * (idx < limit - 1)


def check_index(arr, indx):
    """Check whether index is in bounds and contains an input seat"""
    ny, nx = arr.shape
    iy, ix = indx
    if not in_bounds(iy, ny) * in_bounds(ix, nx):
        stop_it = True
    elif arr[iy, ix] != ".":
        stop_it = True
    else:
        stop_it = False
    return stop_it


def get_subset_part2(array, directions, iy, ix):
    """Search all 8 directions to return the valid adjacent seats."""

    found_seat_in_direction = len(directions) * [False]
    seats = len(directions) * ["."]
    mult = 1    # number of cells along a particular direction to serch
    while not all(found_seat_in_direction):
        # get indices to loop through
        indx = directions * mult + np.array([iy, ix])

        found_seat_in_direction, seats = update_found_seats(array, found_seat_in_direction, indx,
                                                            seats)
        mult += 1
    return seats


def update_found_seats(array, found_seat_in_direction, indx, seats):
    """Loop over directions if valid seat is found add it to list of seats """
    for ii, idx in enumerate(indx):

        if not found_seat_in_direction[ii]:
            stop_it = check_index(array, idx)
            if stop_it:
                seats[ii] = array[idx[0], idx[1]]

            found_seat_in_direction[ii] = stop_it
    return found_seat_in_direction, seats


def swap_full_and_empty(padded_array, swap_h, swap_l):
    for i1, i2 in swap_l:
        padded_array[i1, i2] = "#"
    for i1, i2 in swap_h:
        padded_array[i1, i2] = "L"
    return padded_array


def get_answer(data, question_part):
    padded_array = pad_data(data)
    directions = get_directions()
    while True:
        padded_array, swap_l, swap_h = swap_seats(padded_array, directions, question_part)
        print("padded_array = \n", padded_array[1:-1, 1:-1])
        if len(swap_l) == 0 and len(swap_h) == 0:
            print("number of full seats = ", count_type(padded_array, "#"))
            break
    return padded_array


def main():
    file_name = "day11_test_input.txt"
    file_name = "day11_input.txt"
    data = load_data(file_name)
    data = get_answer(data, question_part=2)


if __name__ == "__main__":
    main()
