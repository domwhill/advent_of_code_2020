"""Advent of code day 9


25 numbers
after that:
each number = sum of any 2 of the 25 previous numbers


Part 2 add the smallest and largest number in this contiguous range.

"""
import numpy as np


def find_summed_numbers(input, target_number):
    """Refactored from day 1"""
    target = target_number - input
    output1, output2 = None, None
    sum_exists = False
    for id, targ in enumerate(target):
        if (targ in input) and targ - input[id] != 0:
            output1 = targ
            output2 = input[id]
            sum_exists = True
            break
    return output1, output2, sum_exists


def get_number_subset(data, index, preamble):
    if index < preamble:
        raise ValueError(f"Looping over preamble data")
    return data[index - preamble:index]


def convolution(data, window_size, target):
    """Perform a convolution between rectangular window of 1s with data

    If convolution equals target value at any point, exit.
    """
    window = np.zeros((len(data)))
    window[:window_size] = 1.0
    output = None
    for i in range(len(data) - window_size):
        convol = np.sum(data[i:i + window_size])
        if convol == target:
            subset = data[i:i + window_size]
            _sum = np.min(subset) + np.max(subset)

            output = (i, i + window_size, _sum)
            break
    return output


def find_contiguous_subset(data, target):
    """Perform convolution with window function of varying width"""
    output = None
    for window_size in range(3, 25):
        output = convolution(data, window_size, target)
        if output is not None:
            print(
                f"data index range = {data[output[0]]}, {data[output[1]]} Sum of max and min values = {output[2]}"
            )
            break
    return output


def check_entry_validity(data, index, preamble):
    target = data[index]
    subset = get_number_subset(data, index, preamble)
    num1, num2, sum_exists = find_summed_numbers(subset, target)
    return sum_exists


def find_first_entry_violation(data, preamble):
    """Look for first number in data that violates summation rule.

    """
    exit_index = None
    for index in range(preamble, len(data)):
        sum_exists = check_entry_validity(data, index, preamble)
        if not sum_exists:
            print(f"Found violation at index {index} entry = {data[index]}")
            exit_index = index
            break
    return exit_index


def main():
    file_name = "day9_input.txt"
    data = np.loadtxt(file_name, dtype=int)
    preamble = 25
    first_violation_index = find_first_entry_violation(data, preamble)
    print("Answer to part 1: violation number = ", data[first_violation_index])

    # part 2
    target = 177777905
    violating_sum = find_contiguous_subset(data, target)
    print(f"Answer to part 2 = {violating_sum[2]}")


if __name__ == "__main__":
    main()
