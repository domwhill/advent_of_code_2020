"""
day 2 -advent of code 2020

Lazy mans processing of passwords
"""
import re
import numpy as np


def process_line(line):
    """Process line input data and return values in schema.


    index1, index2, letter, password
    """
    processed_line = np.array(re.sub("-|\s", ":", line).split(":"))
    processed_line = processed_line[processed_line != ""]
    min_l, max_l, letter, password = processed_line
    return int(min_l), int(max_l), letter, password


def check_validity_1(min_l, max_l, letter, password):
    """Check password validity for the first part of the question.

    Letter count in password must satisfy: min_l<= letter # <= max_l
    """
    num_counts = password.count(letter)
    return (num_counts >= min_l) * (num_counts <= max_l)


def check_validity_2(min_l, max_l, letter, password):
    """Check password validity for the second part of the question

    Only one of positions min_l and max_l in password should contain letter
    """
    # convert to index
    imin, imax = min_l - 1, max_l - 1
    # deal with case that the index is
    # larger than the password
    if imax >= len(password):
        return False
    # Looking for one True
    # Not allowed: (True, true), (false, false)
    bool_1 = bool(password[imin] == letter)
    bool_2 = bool(password[imax] == letter)
    return bool_1 != bool_2


def get_valid_password_number(file_name):
    """ Process all passwords from file and count the number of valid ones.

    file_name = path to input data
    """
    f = open(file_name, "r")
    valid_list = []
    for line in f.readlines():
        processed_line = process_line(line)
        # min_num, max_num, letter, password
        is_valid = check_validity_2(*processed_line)
        valid_list.append(is_valid)
    f.close()
    return np.sum(valid_list)


if __name__ == "__main__":
    #file_name = "test_input2.txt"
    file_name = "day2_input.txt"
    number_of_valid_pw = get_valid_password_number(file_name)
    print("answer = ", number_of_valid_pw)
