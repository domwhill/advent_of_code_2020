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


def construct_window():
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


def swap_seats_part1(padded_array, window):
    swap_l = []
    swap_h = []
    ny, nx = padded_array.shape
    for ix in range(1, nx - 1):
        for iy in range(1, ny - 1):
            val = padded_array[iy, ix]
            if val == ".":
                continue

            _subset = get_subset(padded_array, window, iy, ix)

            num_empty = count_type(_subset, "L")
            num_full = count_type(_subset, "#")
            if val == "L" and num_full == 0:
                swap_l.append((iy, ix))
            elif val == "#" and num_full >= 4:
                swap_h.append((iy, ix))

    padded_array = swap_full_and_empty(padded_array, swap_h, swap_l)

    return padded_array, swap_l, swap_h


def get_subset(array, window, iy, ix):
    """Search all 8 directions to return the valid adjacent seats."""
    indx = window + np.array([iy, ix])
    _subset = [array[i1, i2] for (i1, i2) in indx]
    return _subset


def swap_full_and_empty(padded_array, swap_h, swap_l):
    for i1, i2 in swap_l:
        padded_array[i1, i2] = "#"
    for i1, i2 in swap_h:
        padded_array[i1, i2] = "L"
    return padded_array


def part1(data):
    padded_array = pad_data(data)
    window = construct_window()
    while True:
        padded_array, swap_l, swap_h = swap_seats_part1(padded_array, window)
        print("padded_array = \n", padded_array[1:-1, 1:-1])
        if len(swap_l) == 0 and len(swap_h) == 0:
            print("number of full seats = ", count_type(padded_array, "#"))
            break
    return padded_array


def main():
    file_name = "day11_test_input.txt"
    file_name = "day11_input.txt"
    data = load_data(file_name)
    data = part1(data)


if __name__ == "__main__":
    main()
