"""Lazy mans advent of code day 1

used itertools instead of recursive functions.
"""
import numpy as np
import itertools


def find_2020(input, target_number=2020):
    """Part 1 find 2 values in list that sum to 2020"""
    target = target_number - input
    output1, output2 = None, None
    for id, targ in enumerate(target):
        if (targ in input) and targ - input[id] != 0:
            output1 = targ
            output2 = input[id]
            break
    return output1, output2


def find_2020_3(test_input, target_number=2020):
    """part 2 find 3 values to sum to 2020"""
    l_i = len(test_input)
    inp = list(itertools.permutations(np.arange(l_i), 3))
    id = np.argwhere(np.sum(test_input[inp], axis=1) == target_number)
    indices = np.array(inp)[id].astype(int).tolist()[0][0]

    return test_input[indices]


if __name__ == "__main__":
    fname = "day1_input.txt"

    input = np.loadtxt(fname).astype(int)
    out1, out2 = find_2020(input)
    print("answer 1 = ", out1 * out2)

    out1, out2, out3 = find_2020_3(input)
    print("answer2 = ", out1 * out2 * out3)
