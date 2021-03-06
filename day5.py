"""
FBFBBFFRLR

First 7 characters FB
- 128 rows (0-127

Last 3 characters will be either L or R
- specify one of 8 columns

Part 2 looking for the only missing boarding pass on the list
"""
import numpy as np
import pytest


def bisect_range(min_val, max_val, upper_or_lower):
    """ """
    # In the case that interval max_val + min_val = #.5 then
    # we want to round up
    bisection = int(np.round((max_val + min_val) / 2))
    if upper_or_lower in ("B", "R"):
        new_range = (bisection, max_val)
    elif upper_or_lower in ("F", "L"):
        new_range = (min_val, bisection)
    else:
        raise ValueError(f"{upper_or_lower} not recognised")
    return new_range


def get_final_seat(min_val, max_val, upper_or_lower):
    """ """
    bisection = int(np.round((max_val + min_val) / 2))

    if upper_or_lower in ("B", "R"):
        # This must be value -1 because we compute the range is not inclusive
        # min_val:max_val = min_val + 0.... max_val-1
        output = max_val - 1
    elif upper_or_lower in ("F", "L"):
        output = min_val
    else:
        raise ValueError(f"{upper_or_lower} not recognised")
    return output


def get_unique_id(row, column):
    return row * 8 + column


def get_seat_row(input):
    min_val, max_val = 0, 127
    assert len(input) == 7
    seat = get_seat_position_1d(input, max_val, min_val)
    return seat


def get_seat_column(input):
    min_val, max_val = 0, 8
    assert len(input) == 3
    seat = get_seat_position_1d(input, max_val, min_val)
    return seat


def get_seat_position_1d(input, max_val, min_val):
    """Get the seat position for either a row or column

    input: string of instructions (F,B) for rows or (L,R) for columns
    min_val,max_val = integers indicating the min max of the search range
    """
    for i in range(len(input) - 1):
        min_val, max_val = bisect_range(min_val, max_val, input[i])

    seat = get_final_seat(min_val, max_val, input[-1])
    return seat


def get_seat_position_2d(input):
    row = get_seat_row(input[:7])
    col = get_seat_column(input[7:])
    id = get_unique_id(row, col)
    return (row, col, id)


@pytest.mark.parametrize("input,expected", [
    ("FBFBBFFRLR", (44, 5, 357)),
    ("BFFFBBFRRR", (70, 7, 567)),
    ("FFFBBBFRRR", (14, 7, 119)),
    ("BBFFBBFRLL", (102, 4, 820)),
])
def test_get_seat_id(input, expected):
    row, col, id = get_seat_position_2d(input)
    print(f"input = {input} row = {row}, col = {col}, id = {id}, expected = {expected}")
    assert row == expected[0]
    assert col == expected[1]
    assert id == expected[2]


def get_max_and_gap_seat_id(file_name):
    """Return the maximum seat id, answer to puzzle part 1"""
    id_list = get_seat_ids(file_name)
    gap_id = get_gap_in_seat_ids(id_list)
    return np.max(id_list), gap_id


def get_gap_in_seat_ids(ids):
    """Sorts seat ids and looks for a gap in the ids of 2 (indicating an unfilled seat)."""
    sorted_ids = np.unique(ids)
    id_diff = sorted_ids[1:] - sorted_ids[:-1]
    # get indices of seats which are on either side of a seat id gap of 2
    lower_seat_index = np.where(id_diff.astype(int) == 2)[0][0]
    upper_seat_index = lower_seat_index + 1

    # Compute the id of the seat in the middle of this gap.
    my_seat_id = (sorted_ids[lower_seat_index] + sorted_ids[upper_seat_index]) // 2
    return my_seat_id


def get_seat_ids(file_name):
    f = open(file_name, "r")
    id_list = []
    for line in f:
        row, col, id = get_seat_position_2d(line.strip())
        id_list.append(id)
    return id_list


def main():
    file_name = "day5_input.txt"
    max_seat_id, my_seat_id = get_max_and_gap_seat_id(file_name)
    print(f"1) max_seat_id = {max_seat_id}")
    print(f"2) my_seat_id = {my_seat_id}")


if __name__ == "__main__":
    main()
