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
    return data[index-preamble:index]

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
    file_name = "test_input_day9.txt"
    file_name = "day9_input.txt"
    data = np.loadtxt(file_name,dtype=int)
    preamble = 25
    first_violation_index = find_first_entry_violation(data, preamble)

    print("violation number = ", data[first_violation_index])

if __name__=="__main__":
    main()
